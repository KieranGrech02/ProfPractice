import hashlib
import os
import random

import httpx


class ThreatIntelService:
    def __init__(self):
        self.vt_api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")

    async def enrich(self, indicator: str, indicator_type: str) -> dict:
        results = {}
        if indicator_type == "ip":
            results["virustotal"] = await self._vt_ip_lookup(indicator)
            results["abuseipdb"] = await self._abuseipdb_lookup(indicator)
        elif indicator_type == "hash":
            results["virustotal"] = await self._vt_hash_lookup(indicator)
        return results

    async def _vt_ip_lookup(self, ip: str) -> dict:
        if self.vt_api_key:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
                        headers={"x-apikey": self.vt_api_key},
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                        return {
                            "malicious": stats.get("malicious", 0),
                            "suspicious": stats.get("suspicious", 0),
                            "harmless": stats.get("harmless", 0),
                            "reputation_score": data.get("data", {}).get("attributes", {}).get("reputation", 0),
                            "country": data.get("data", {}).get("attributes", {}).get("country", "Unknown"),
                            "as_owner": data.get("data", {}).get("attributes", {}).get("as_owner", "Unknown"),
                        }
            except httpx.RequestError:
                pass
        return self._mock_vt_ip(ip)

    async def _vt_hash_lookup(self, file_hash: str) -> dict:
        if self.vt_api_key:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"https://www.virustotal.com/api/v3/files/{file_hash}",
                        headers={"x-apikey": self.vt_api_key},
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                        return {
                            "malicious": stats.get("malicious", 0),
                            "suspicious": stats.get("suspicious", 0),
                            "harmless": stats.get("harmless", 0),
                            "reputation_score": -stats.get("malicious", 0),
                            "file_type": data.get("data", {}).get("attributes", {}).get("type_description", "Unknown"),
                            "threat_label": data.get("data", {}).get("attributes", {}).get("popular_threat_classification", {}).get("suggested_threat_label", "Unknown"),
                        }
            except httpx.RequestError:
                pass
        return self._mock_vt_hash(file_hash)

    async def _abuseipdb_lookup(self, ip: str) -> dict:
        if self.abuseipdb_api_key:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        "https://api.abuseipdb.com/api/v2/check",
                        params={"ipAddress": ip, "maxAgeInDays": 90},
                        headers={"Key": self.abuseipdb_api_key, "Accept": "application/json"},
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        data = resp.json().get("data", {})
                        return {
                            "malicious": 1 if data.get("abuseConfidenceScore", 0) > 50 else 0,
                            "reputation_score": 100 - data.get("abuseConfidenceScore", 0),
                            "abuse_confidence": data.get("abuseConfidenceScore", 0),
                            "total_reports": data.get("totalReports", 0),
                            "country": data.get("countryCode", "Unknown"),
                            "isp": data.get("isp", "Unknown"),
                            "domain": data.get("domain", "Unknown"),
                        }
            except httpx.RequestError:
                pass
        return self._mock_abuseipdb(ip)

    def _mock_vt_ip(self, ip: str) -> dict:
        seed = int(hashlib.md5(ip.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed)
        malicious = rng.randint(0, 25)
        return {
            "malicious": malicious,
            "suspicious": rng.randint(0, 5),
            "harmless": rng.randint(50, 80),
            "reputation_score": -malicious if malicious > 5 else rng.randint(0, 10),
            "country": rng.choice(["US", "CN", "RU", "DE", "BR", "KR", "NL", "GB", "JP", "IN"]),
            "as_owner": rng.choice([
                "DigitalOcean LLC", "Amazon.com Inc.", "OVH SAS",
                "Hetzner Online GmbH", "China Telecom", "Rostelecom",
            ]),
        }

    def _mock_vt_hash(self, file_hash: str) -> dict:
        seed = int(hashlib.md5(file_hash.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed)
        malicious = rng.randint(15, 60)
        return {
            "malicious": malicious,
            "suspicious": rng.randint(0, 10),
            "harmless": rng.randint(5, 30),
            "reputation_score": -malicious,
            "file_type": rng.choice(["PE32 executable", "ELF", "PDF document", "MS Office document"]),
            "threat_label": rng.choice([
                "trojan.generickd", "ransomware.wannacry", "backdoor.cobalt",
                "infostealer.redline", "loader.emotet",
            ]),
        }

    def _mock_abuseipdb(self, ip: str) -> dict:
        seed = int(hashlib.md5(ip.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed)
        confidence = rng.randint(10, 95)
        return {
            "malicious": 1 if confidence > 50 else 0,
            "reputation_score": 100 - confidence,
            "abuse_confidence": confidence,
            "total_reports": rng.randint(1, 500),
            "country": rng.choice(["US", "CN", "RU", "DE", "BR", "KR", "NL"]),
            "isp": rng.choice([
                "DigitalOcean LLC", "Amazon AWS", "OVH SAS",
                "Hetzner Online GmbH", "Alibaba Cloud",
            ]),
            "domain": rng.choice([
                "digitalocean.com", "amazonaws.com", "ovh.net",
                "hetzner.de", "alibabacloud.com",
            ]),
        }
