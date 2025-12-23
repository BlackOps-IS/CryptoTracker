"""
Utility functions for CryptoTracker
"""
from datetime import datetime
from typing import Dict, List
import json

def format_address(address: str, length: int = 10) -> str:
    """
    Format address for display (0x1234...5678)
    """
    if not address:
        return "N/A"
    
    if len(address) <= length * 2:
        return address
    
    return f"{address[:length]}...{address[-length:]}"

def format_timestamp(timestamp: int) -> str:
    """
    Format Unix timestamp to readable date
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return "N/A"

def format_currency(amount: float, decimals: int = 2) -> str:
    """
    Format currency amount with commas
    """
    return f"${amount:,.{decimals}f}"

def format_eth(amount: float, decimals: int = 4) -> str:
    """
    Format ETH amount
    """
    return f"{amount:.{decimals}f} ETH"

def calculate_time_elapsed(timestamp: int) -> str:
    """
    Calculate time elapsed since timestamp
    """
    try:
        dt = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        diff = now - dt
        
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        
        if days > 0:
            return f"{days} days, {hours} hours ago"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes ago"
        else:
            return f"{minutes} minutes ago"
    except:
        return "N/A"

def validate_ethereum_address(address: str) -> bool:
    """
    Validate Ethereum address format
    """
    if not address:
        return False
    
    # Remove 0x prefix if present
    if address.startswith('0x'):
        address = address[2:]
    
    # Check length (40 hex characters)
    if len(address) != 40:
        return False
    
    # Check if all characters are hex
    try:
        int(address, 16)
        return True
    except ValueError:
        return False

def validate_transaction_hash(tx_hash: str) -> bool:
    """
    Validate transaction hash format
    """
    if not tx_hash:
        return False
    
    # Remove 0x prefix if present
    if tx_hash.startswith('0x'):
        tx_hash = tx_hash[2:]
    
    # Check length (64 hex characters)
    if len(tx_hash) != 64:
        return False
    
    # Check if all characters are hex
    try:
        int(tx_hash, 16)
        return True
    except ValueError:
        return False

def get_risk_color(risk_level: str) -> str:
    """
    Get color code for risk level
    """
    colors = {
        'CRITICAL': '#dc3545',
        'HIGH': '#fd7e14',
        'MEDIUM': '#ffc107',
        'LOW': '#28a745',
        'MINIMAL': '#17a2b8'
    }
    return colors.get(risk_level, '#6c757d')

def export_to_json(data: Dict, filename: str) -> bool:
    """
    Export data to JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False

def generate_report_filename(prefix: str = "report") -> str:
    """
    Generate timestamped filename for reports
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.json"

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input
    """
    if not input_str:
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = input_str.strip()
    
    # Convert to lowercase for addresses
    if validate_ethereum_address(sanitized) or validate_transaction_hash(sanitized):
        sanitized = sanitized.lower()
    
    return sanitized

def calculate_percentage(part: float, whole: float) -> float:
    """
    Calculate percentage safely
    """
    if whole == 0:
        return 0
    return (part / whole) * 100

def format_large_number(number: int) -> str:
    """
    Format large numbers with K, M, B suffixes
    """
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.2f}K"
    else:
        return str(number)

def get_explorer_url(address: str, network: str = 'ethereum') -> str:
    """
    Get blockchain explorer URL for address
    """
    explorers = {
        'ethereum': f'https://etherscan.io/address/{address}',
        'bsc': f'https://bscscan.com/address/{address}',
        'polygon': f'https://polygonscan.com/address/{address}'
    }
    return explorers.get(network, explorers['ethereum'])

def get_tx_explorer_url(tx_hash: str, network: str = 'ethereum') -> str:
    """
    Get blockchain explorer URL for transaction
    """
    explorers = {
        'ethereum': f'https://etherscan.io/tx/{tx_hash}',
        'bsc': f'https://bscscan.com/tx/{tx_hash}',
        'polygon': f'https://polygonscan.com/tx/{tx_hash}'
    }
    return explorers.get(network, explorers['ethereum'])