"""
Advanced Blockchain Analysis Engine
Tracks transactions, detects address poisoning, and identifies mixer usage
"""
import requests
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from web3 import Web3
from config import Config

class BlockchainAnalyzer:
    """
    Core blockchain analysis engine for tracking transactions and detecting threats
    """
    
    def __init__(self, api_key: str = None, network: str = 'ethereum'):
        self.api_key = api_key or Config.ETHERSCAN_API_KEY
        self.network = network
        self.base_url = self._get_base_url(network)
        self.w3 = self._init_web3(network)
        self.request_delay = 0.2  # Rate limiting
        
    def _get_base_url(self, network: str) -> str:
        """Get the appropriate API base URL for the network"""
        urls = {
            'ethereum': 'https://api.etherscan.io/api',
            'bsc': 'https://api.bscscan.com/api',
            'polygon': 'https://api.polygonscan.com/api'
        }
        return urls.get(network, urls['ethereum'])
    
    def _init_web3(self, network: str) -> Web3:
        """Initialize Web3 connection"""
        rpcs = {
            'ethereum': Config.ETHEREUM_RPC_URL,
            'bsc': Config.BSC_RPC_URL,
            'polygon': Config.POLYGON_RPC_URL
        }
        return Web3(Web3.HTTPProvider(rpcs.get(network, rpcs['ethereum'])))
    
    def _make_request(self, params: Dict) -> Dict:
        """Make API request with rate limiting"""
        time.sleep(self.request_delay)
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'status': '0', 'message': f'Request failed: {str(e)}', 'result': []}
    
    def get_transaction_details(self, tx_hash: str) -> Optional[Dict]:
        """Get detailed information about a specific transaction"""
        params = {
            'module': 'proxy',
            'action': 'eth_getTransactionByHash',
            'txhash': tx_hash
        }
        
        data = self._make_request(params)
        if data.get('result'):
            tx = data['result']
            
            # Get transaction receipt for status
            receipt_params = {
                'module': 'proxy',
                'action': 'eth_getTransactionReceipt',
                'txhash': tx_hash
            }
            receipt_data = self._make_request(receipt_params)
            
            return {
                'hash': tx.get('hash'),
                'from': tx.get('from'),
                'to': tx.get('to'),
                'value': int(tx.get('value', '0'), 16) / 1e18,  # Convert to ETH
                'gas': int(tx.get('gas', '0'), 16),
                'gasPrice': int(tx.get('gasPrice', '0'), 16) / 1e9,  # Convert to Gwei
                'input': tx.get('input'),
                'blockNumber': int(tx.get('blockNumber', '0'), 16),
                'status': receipt_data.get('result', {}).get('status') == '0x1',
                'timestamp': self._get_block_timestamp(int(tx.get('blockNumber', '0'), 16))
            }
        return None
    
    def _get_block_timestamp(self, block_number: int) -> int:
        """Get timestamp for a block"""
        params = {
            'module': 'proxy',
            'action': 'eth_getBlockByNumber',
            'tag': hex(block_number),
            'boolean': 'false'
        }
        
        data = self._make_request(params)
        if data.get('result'):
            return int(data['result'].get('timestamp', '0'), 16)
        return 0
    
    def get_transaction_history(self, address: str, start_block: int = 0, 
                                end_block: int = 99999999) -> List[Dict]:
        """Get transaction history for an address"""
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'sort': 'desc'
        }
        
        data = self._make_request(params)
        if data.get('status') == '1':
            return data.get('result', [])
        return []
    
    def get_internal_transactions(self, address: str) -> List[Dict]:
        """Get internal transactions (contract interactions)"""
        params = {
            'module': 'account',
            'action': 'txlistinternal',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'desc'
        }
        
        data = self._make_request(params)
        if data.get('status') == '1':
            return data.get('result', [])
        return []
    
    def get_token_transfers(self, address: str) -> List[Dict]:
        """Get ERC-20 token transfer history"""
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'desc'
        }
        
        data = self._make_request(params)
        if data.get('status') == '1':
            return data.get('result', [])
        return []
    
    def detect_address_poisoning(self, victim_address: str) -> Dict:
        """
        Detect potential address poisoning attacks
        Returns suspicious addresses and risk assessment
        """
        transactions = self.get_transaction_history(victim_address)
        
        # Get addresses that have sent to the victim
        incoming_addresses = {}
        for tx in transactions:
            if tx['to'].lower() == victim_address.lower():
                sender = tx['from'].lower()
                if sender not in incoming_addresses:
                    incoming_addresses[sender] = []
                incoming_addresses[sender].append(tx)
        
        # Look for similar addresses (address poisoning pattern)
        similar_addresses = []
        victim_lower = victim_address.lower()
        
        for addr in incoming_addresses.keys():
            similarity_score = self._calculate_address_similarity(victim_lower, addr)
            
            # Check for poisoning patterns
            if similarity_score > 0:
                txs = incoming_addresses[addr]
                
                # Poisoning indicators:
                # 1. Very small amounts (dust transactions)
                # 2. Multiple transactions from same address
                # 3. High similarity to victim's address
                
                avg_value = sum(float(tx.get('value', 0)) for tx in txs) / len(txs) if txs else 0
                
                if avg_value < 0.0001 and len(txs) > 1:  # Dust transactions
                    similar_addresses.append({
                        'address': addr,
                        'similarity_score': similarity_score,
                        'transaction_count': len(txs),
                        'average_value': avg_value,
                        'risk_level': 'HIGH',
                        'pattern': 'Address Poisoning'
                    })
        
        return {
            'victim_address': victim_address,
            'suspicious_addresses': similar_addresses,
            'total_suspicious': len(similar_addresses),
            'risk_assessment': 'HIGH' if similar_addresses else 'LOW'
        }
    
    def _calculate_address_similarity(self, addr1: str, addr2: str) -> int:
        """
        Calculate similarity between two addresses
        Returns number of matching characters at start and end
        """
        addr1 = addr1.lower().replace('0x', '')
        addr2 = addr2.lower().replace('0x', '')
        
        # Check first N characters
        start_match = 0
        for i in range(min(Config.SIMILAR_ADDRESS_THRESHOLD, len(addr1), len(addr2))):
            if addr1[i] == addr2[i]:
                start_match += 1
            else:
                break
        
        # Check last N characters
        end_match = 0
        for i in range(1, min(Config.SIMILAR_ADDRESS_THRESHOLD + 1, len(addr1), len(addr2))):
            if addr1[-i] == addr2[-i]:
                end_match += 1
            else:
                break
        
        return start_match + end_match
    
    def detect_mixer_usage(self, address: str) -> Dict:
        """
        Detect if an address has interacted with known mixers (Tornado Cash, etc.)
        """
        transactions = self.get_transaction_history(address)
        internal_txs = self.get_internal_transactions(address)
        
        all_txs = transactions + internal_txs
        
        mixer_interactions = []
        
        for tx in all_txs:
            tx_to = tx.get('to', '').lower()
            tx_from = tx.get('from', '').lower()
            
            # Check if transaction involves known mixer
            for mixer_addr in Config.TORNADO_CASH_ADDRESSES:
                mixer_lower = mixer_addr.lower()
                
                if tx_to == mixer_lower or tx_from == mixer_lower:
                    mixer_interactions.append({
                        'hash': tx.get('hash'),
                        'mixer_address': mixer_addr,
                        'mixer_name': 'Tornado Cash',
                        'direction': 'deposit' if tx_to == mixer_lower else 'withdrawal',
                        'value': float(tx.get('value', 0)) / 1e18,
                        'timestamp': tx.get('timeStamp'),
                        'block': tx.get('blockNumber')
                    })
        
        return {
            'address': address,
            'mixer_detected': len(mixer_interactions) > 0,
            'total_interactions': len(mixer_interactions),
            'interactions': mixer_interactions,
            'risk_level': 'HIGH' if mixer_interactions else 'LOW'
        }
    
    def detect_exchange_interaction(self, address: str) -> Dict:
        """
        Detect if funds have been sent to known exchanges
        This is crucial for recovery efforts
        """
        transactions = self.get_transaction_history(address)
        
        exchange_interactions = []
        
        for tx in transactions:
            tx_to = tx.get('to', '').lower()
            
            if tx_to in Config.KNOWN_EXCHANGES:
                exchange_interactions.append({
                    'hash': tx.get('hash'),
                    'exchange': Config.KNOWN_EXCHANGES[tx_to],
                    'exchange_address': tx_to,
                    'value': float(tx.get('value', 0)) / 1e18,
                    'timestamp': tx.get('timeStamp'),
                    'block': tx.get('blockNumber'),
                    'status': 'Funds may be recoverable - contact exchange immediately'
                })
        
        return {
            'address': address,
            'exchange_detected': len(exchange_interactions) > 0,
            'total_interactions': len(exchange_interactions),
            'interactions': exchange_interactions,
            'recovery_potential': 'HIGH' if exchange_interactions else 'MEDIUM'
        }
    
    def trace_funds(self, start_address: str, max_depth: int = None) -> Dict:
        """
        Trace the flow of funds from a starting address
        Returns a graph of transactions
        """
        max_depth = max_depth or Config.MAX_TRANSACTION_DEPTH
        
        visited = set()
        trace_graph = {
            'nodes': [],
            'edges': [],
            'metadata': {
                'start_address': start_address,
                'max_depth': max_depth,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        def trace_recursive(address: str, depth: int):
            if depth > max_depth or address.lower() in visited:
                return
            
            visited.add(address.lower())
            
            # Add node
            trace_graph['nodes'].append({
                'address': address,
                'depth': depth,
                'label': self._get_address_label(address)
            })
            
            # Get outgoing transactions
            transactions = self.get_transaction_history(address)
            
            for tx in transactions[:50]:  # Limit to prevent excessive API calls
                if tx['from'].lower() == address.lower():
                    to_address = tx['to']
                    
                    # Add edge
                    trace_graph['edges'].append({
                        'from': address,
                        'to': to_address,
                        'value': float(tx.get('value', 0)) / 1e18,
                        'hash': tx.get('hash'),
                        'timestamp': tx.get('timeStamp')
                    })
                    
                    # Recurse
                    if depth < max_depth:
                        trace_recursive(to_address, depth + 1)
        
        trace_recursive(start_address, 0)
        
        return trace_graph
    
    def _get_address_label(self, address: str) -> str:
        """Get a human-readable label for an address"""
        addr_lower = address.lower()
        
        # Check if it's a known exchange
        if addr_lower in Config.KNOWN_EXCHANGES:
            return Config.KNOWN_EXCHANGES[addr_lower]
        
        # Check if it's a known mixer
        if addr_lower in [m.lower() for m in Config.TORNADO_CASH_ADDRESSES]:
            return 'Tornado Cash'
        
        # Check if it's a contract
        code = self.w3.eth.get_code(Web3.to_checksum_address(address))
        if code and code != b'':
            return 'Smart Contract'
        
        return 'EOA (Wallet)'
    
    def analyze_transaction_pattern(self, address: str) -> Dict:
        """
        Analyze transaction patterns to identify suspicious behavior
        """
        transactions = self.get_transaction_history(address)
        
        if not transactions:
            return {
                'address': address,
                'pattern': 'No transactions found',
                'risk_score': 0
            }
        
        # Calculate various metrics
        total_txs = len(transactions)
        total_value_sent = sum(float(tx.get('value', 0)) for tx in transactions if tx['from'].lower() == address.lower())
        total_value_received = sum(float(tx.get('value', 0)) for tx in transactions if tx['to'].lower() == address.lower())
        
        # Check for rapid transactions (potential automated behavior)
        timestamps = [int(tx.get('timeStamp', 0)) for tx in transactions]
        timestamps.sort()
        
        rapid_txs = 0
        for i in range(1, len(timestamps)):
            if timestamps[i] - timestamps[i-1] < 60:  # Less than 1 minute apart
                rapid_txs += 1
        
        # Calculate risk score
        risk_score = 0
        risk_factors = []
        
        if rapid_txs > 10:
            risk_score += 20
            risk_factors.append('High frequency of rapid transactions')
        
        if total_value_sent > total_value_received * 1.5:
            risk_score += 15
            risk_factors.append('Significantly more value sent than received')
        
        # Check for mixer usage
        mixer_check = self.detect_mixer_usage(address)
        if mixer_check['mixer_detected']:
            risk_score += 40
            risk_factors.append('Mixer usage detected')
        
        # Check for address poisoning
        poisoning_check = self.detect_address_poisoning(address)
        if poisoning_check['total_suspicious'] > 0:
            risk_score += 25
            risk_factors.append('Potential address poisoning activity')
        
        return {
            'address': address,
            'total_transactions': total_txs,
            'total_value_sent': total_value_sent / 1e18,
            'total_value_received': total_value_received / 1e18,
            'rapid_transactions': rapid_txs,
            'risk_score': min(risk_score, 100),
            'risk_level': self._get_risk_level(risk_score),
            'risk_factors': risk_factors,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to risk level"""
        if score >= Config.RISK_SCORE_HIGH:
            return 'HIGH'
        elif score >= Config.RISK_SCORE_MEDIUM:
            return 'MEDIUM'
        elif score >= Config.RISK_SCORE_LOW:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def get_address_balance(self, address: str) -> Dict:
        """Get current balance of an address"""
        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest'
        }
        
        data = self._make_request(params)
        if data.get('status') == '1':
            balance_wei = int(data.get('result', 0))
            return {
                'address': address,
                'balance_wei': balance_wei,
                'balance_eth': balance_wei / 1e18,
                'timestamp': datetime.now().isoformat()
            }
        return {'address': address, 'balance_eth': 0, 'error': 'Failed to fetch balance'}