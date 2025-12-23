"""
OSINT (Open Source Intelligence) Collection System
Gathers publicly available information about cryptocurrency addresses
"""
import requests
import time
from typing import Dict, List, Optional
from datetime import datetime
import json

class OSINTCollector:
    """
    Collects open source intelligence about cryptocurrency addresses
    Only uses publicly available, legally obtainable information
    """
    
    def __init__(self, etherscan_api_key: str = None):
        self.etherscan_api_key = etherscan_api_key
        self.cache = {}
        self.cache_duration = 3600  # 1 hour
        
    def collect_all_osint(self, address: str) -> Dict:
        """
        Collect all available OSINT for an address
        """
        return {
            'address': address,
            'timestamp': datetime.now().isoformat(),
            'on_chain_data': self.get_on_chain_intelligence(address),
            'public_labels': self.get_public_labels(address),
            'threat_intelligence': self.get_threat_intelligence(address),
            'social_mentions': self.search_public_mentions(address),
            'risk_assessment': self.calculate_risk_assessment(address)
        }
    
    def get_on_chain_intelligence(self, address: str) -> Dict:
        """
        Gather on-chain intelligence about an address
        """
        # Check cache
        cache_key = f"onchain_{address}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        intelligence = {
            'address_type': self._determine_address_type(address),
            'first_seen': None,
            'last_seen': None,
            'total_transactions': 0,
            'unique_interactions': 0,
            'contract_interactions': [],
            'token_holdings': []
        }
        
        # Get transaction history to determine first/last seen
        try:
            params = {
                'module': 'account',
                'action': 'txlist',
                'address': address,
                'startblock': 0,
                'endblock': 99999999,
                'sort': 'asc',
                'apikey': self.etherscan_api_key
            }
            
            response = requests.get('https://api.etherscan.io/api', params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == '1' and data.get('result'):
                transactions = data['result']
                intelligence['total_transactions'] = len(transactions)
                
                if transactions:
                    intelligence['first_seen'] = datetime.fromtimestamp(
                        int(transactions[0].get('timeStamp', 0))
                    ).isoformat()
                    intelligence['last_seen'] = datetime.fromtimestamp(
                        int(transactions[-1].get('timeStamp', 0))
                    ).isoformat()
                    
                    # Count unique interactions
                    unique_addresses = set()
                    for tx in transactions:
                        unique_addresses.add(tx.get('from'))
                        unique_addresses.add(tx.get('to'))
                    intelligence['unique_interactions'] = len(unique_addresses)
        
        except Exception as e:
            intelligence['error'] = f"Failed to fetch on-chain data: {str(e)}"
        
        # Cache the result
        self.cache[cache_key] = (intelligence, time.time())
        
        return intelligence
    
    def _determine_address_type(self, address: str) -> str:
        """
        Determine if address is EOA or contract
        """
        try:
            params = {
                'module': 'proxy',
                'action': 'eth_getCode',
                'address': address,
                'tag': 'latest',
                'apikey': self.etherscan_api_key
            }
            
            response = requests.get('https://api.etherscan.io/api', params=params, timeout=10)
            data = response.json()
            
            code = data.get('result', '0x')
            if code and code != '0x':
                return 'Smart Contract'
            else:
                return 'EOA (Externally Owned Account)'
        except:
            return 'Unknown'
    
    def get_public_labels(self, address: str) -> Dict:
        """
        Get publicly known labels for an address
        """
        labels = {
            'etherscan_label': None,
            'known_entity': None,
            'tags': []
        }
        
        try:
            # Try to get contract name if it's a contract
            params = {
                'module': 'contract',
                'action': 'getsourcecode',
                'address': address,
                'apikey': self.etherscan_api_key
            }
            
            response = requests.get('https://api.etherscan.io/api', params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == '1' and data.get('result'):
                result = data['result'][0]
                contract_name = result.get('ContractName')
                
                if contract_name:
                    labels['etherscan_label'] = contract_name
                    labels['tags'].append('Verified Contract')
        
        except Exception as e:
            labels['error'] = f"Failed to fetch labels: {str(e)}"
        
        return labels
    
    def get_threat_intelligence(self, address: str) -> Dict:
        """
        Check address against known threat databases
        """
        threat_data = {
            'is_flagged': False,
            'threat_level': 'UNKNOWN',
            'reports': [],
            'sources': []
        }
        
        # Check against known scam databases (using public APIs)
        # Note: In production, you would integrate with services like:
        # - Chainabuse.com
        # - Etherscan's phishing database
        # - SlowMist's blacklist
        
        # For now, we'll check if it's a known mixer
        from config import Config
        
        if address.lower() in [m.lower() for m in Config.TORNADO_CASH_ADDRESSES]:
            threat_data['is_flagged'] = True
            threat_data['threat_level'] = 'HIGH'
            threat_data['reports'].append({
                'type': 'Mixer',
                'description': 'Known Tornado Cash mixer address',
                'severity': 'HIGH'
            })
            threat_data['sources'].append('Internal Database')
        
        # Check if it's a known exchange (not a threat, but important to know)
        if address.lower() in Config.KNOWN_EXCHANGES:
            threat_data['reports'].append({
                'type': 'Exchange',
                'description': f'Known exchange: {Config.KNOWN_EXCHANGES[address.lower()]}',
                'severity': 'INFO'
            })
            threat_data['sources'].append('Internal Database')
        
        return threat_data
    
    def search_public_mentions(self, address: str) -> Dict:
        """
        Search for public mentions of the address
        """
        mentions = {
            'total_found': 0,
            'sources': [],
            'sample_mentions': []
        }
        
        # In a production system, you would search:
        # - Twitter/X (using their API)
        # - Reddit (using their API)
        # - GitHub (using their API)
        # - Crypto forums (web scraping with permission)
        # - News articles (using news APIs)
        
        # For demonstration, we'll note where to look
        mentions['sources'] = [
            'Twitter/X - Search for address mentions',
            'Reddit - r/cryptocurrency, r/ethereum',
            'GitHub - Public repositories',
            'Etherscan - Comments section',
            'Crypto forums - BitcoinTalk, etc.'
        ]
        
        mentions['note'] = 'Manual search recommended for comprehensive results'
        
        return mentions
    
    def calculate_risk_assessment(self, address: str) -> Dict:
        """
        Calculate overall risk assessment based on all collected intelligence
        """
        risk_score = 0
        risk_factors = []
        
        # Get threat intelligence
        threat_intel = self.get_threat_intelligence(address)
        
        if threat_intel['is_flagged']:
            risk_score += 50
            risk_factors.append('Address flagged in threat databases')
        
        # Get on-chain intelligence
        onchain = self.get_on_chain_intelligence(address)
        
        if onchain.get('total_transactions', 0) < 5:
            risk_score += 10
            risk_factors.append('Low transaction history (potential new scam address)')
        
        if onchain.get('address_type') == 'Smart Contract':
            # Contracts aren't inherently risky, but unverified ones are
            labels = self.get_public_labels(address)
            if not labels.get('etherscan_label'):
                risk_score += 15
                risk_factors.append('Unverified smart contract')
        
        # Determine risk level
        if risk_score >= 75:
            risk_level = 'CRITICAL'
        elif risk_score >= 50:
            risk_level = 'HIGH'
        elif risk_score >= 25:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'recommendation': self._get_recommendation(risk_level),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_recommendation(self, risk_level: str) -> str:
        """
        Get recommendation based on risk level
        """
        recommendations = {
            'CRITICAL': 'DO NOT INTERACT - High risk of scam or theft. Report to authorities.',
            'HIGH': 'CAUTION - Significant risk factors detected. Verify thoroughly before any interaction.',
            'MEDIUM': 'VERIFY - Some risk factors present. Conduct additional research before proceeding.',
            'LOW': 'NORMAL - Standard precautions apply. Always verify addresses before sending funds.'
        }
        return recommendations.get(risk_level, 'Unknown risk level')
    
    def generate_osint_report(self, address: str) -> str:
        """
        Generate a comprehensive OSINT report in markdown format
        """
        osint_data = self.collect_all_osint(address)
        
        report = f"""# OSINT Report for Address: {address}

## Report Generated
**Timestamp:** {osint_data['timestamp']}

---

## Risk Assessment
**Risk Level:** {osint_data['risk_assessment']['risk_level']}
**Risk Score:** {osint_data['risk_assessment']['risk_score']}/100
**Recommendation:** {osint_data['risk_assessment']['recommendation']}

### Risk Factors
"""
        
        if osint_data['risk_assessment']['risk_factors']:
            for factor in osint_data['risk_assessment']['risk_factors']:
                report += f"- {factor}\n"
        else:
            report += "- No significant risk factors detected\n"
        
        report += f"""

---

## On-Chain Intelligence
**Address Type:** {osint_data['on_chain_data'].get('address_type', 'Unknown')}
**First Seen:** {osint_data['on_chain_data'].get('first_seen', 'N/A')}
**Last Seen:** {osint_data['on_chain_data'].get('last_seen', 'N/A')}
**Total Transactions:** {osint_data['on_chain_data'].get('total_transactions', 0)}
**Unique Interactions:** {osint_data['on_chain_data'].get('unique_interactions', 0)}

---

## Public Labels
"""
        
        labels = osint_data['public_labels']
        if labels.get('etherscan_label'):
            report += f"**Etherscan Label:** {labels['etherscan_label']}\n"
        if labels.get('known_entity'):
            report += f"**Known Entity:** {labels['known_entity']}\n"
        if labels.get('tags'):
            report += f"**Tags:** {', '.join(labels['tags'])}\n"
        
        if not any([labels.get('etherscan_label'), labels.get('known_entity'), labels.get('tags')]):
            report += "No public labels found\n"
        
        report += f"""

---

## Threat Intelligence
**Flagged:** {'Yes' if osint_data['threat_intelligence']['is_flagged'] else 'No'}
**Threat Level:** {osint_data['threat_intelligence']['threat_level']}

"""
        
        if osint_data['threat_intelligence']['reports']:
            report += "### Reports\n"
            for rep in osint_data['threat_intelligence']['reports']:
                report += f"- **{rep['type']}:** {rep['description']} (Severity: {rep['severity']})\n"
        
        report += f"""

---

## Public Mentions
**Total Found:** {osint_data['social_mentions']['total_found']}

### Recommended Search Sources
"""
        
        for source in osint_data['social_mentions']['sources']:
            report += f"- {source}\n"
        
        report += """

---

## Disclaimer
This report is based on publicly available information and automated analysis. 
It should not be considered as financial or legal advice. Always conduct your own 
research and consult with professionals before making any decisions.

**Note:** OSINT data is collected from public sources only and complies with all 
applicable laws and regulations.
"""
        
        return report
    
    def search_similar_scams(self, pattern: str) -> List[Dict]:
        """
        Search for similar scam patterns in historical data
        """
        # In production, this would query a database of known scams
        # For now, return a template
        
        return [
            {
                'pattern': pattern,
                'description': 'Search historical scam database for similar patterns',
                'recommendation': 'Cross-reference with known attack vectors'
            }
        ]
    
    def get_recovery_contacts(self, address: str) -> Dict:
        """
        Get contact information for recovery efforts
        """
        contacts = {
            'exchanges': [],
            'law_enforcement': [],
            'recovery_services': []
        }
        
        # Check if funds went to known exchanges
        from config import Config
        
        if address.lower() in Config.KNOWN_EXCHANGES:
            exchange_name = Config.KNOWN_EXCHANGES[address.lower()]
            contacts['exchanges'].append({
                'name': exchange_name,
                'action': 'Contact immediately with transaction details',
                'urgency': 'HIGH'
            })
        
        # Add general recovery contacts
        contacts['recovery_services'] = [
            {
                'name': 'Chainalysis',
                'service': 'Blockchain forensics',
                'website': 'https://www.chainalysis.com'
            },
            {
                'name': 'TRM Labs',
                'service': 'Crypto compliance and investigations',
                'website': 'https://www.trmlabs.com'
            },
            {
                'name': 'CipherBlade',
                'service': 'Crypto investigation and recovery',
                'website': 'https://cipherblade.com'
            }
        ]
        
        contacts['law_enforcement'] = [
            {
                'agency': 'FBI Internet Crime Complaint Center (IC3)',
                'website': 'https://www.ic3.gov',
                'note': 'For US-based victims'
            },
            {
                'agency': 'Local Police Department',
                'note': 'File a report with your local authorities'
            }
        ]
        
        return contacts