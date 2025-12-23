"""
Configuration management for CryptoTracker
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Blockchain API Keys
    ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '')
    BSCSCAN_API_KEY = os.getenv('BSCSCAN_API_KEY', '')
    POLYGONSCAN_API_KEY = os.getenv('POLYGONSCAN_API_KEY', '')
    
    # Web3 Providers
    ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL', 'https://eth.llamarpc.com')
    BSC_RPC_URL = os.getenv('BSC_RPC_URL', 'https://bsc-dataseed.binance.org/')
    POLYGON_RPC_URL = os.getenv('POLYGON_RPC_URL', 'https://polygon-rpc.com/')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///cryptotracker.db')
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    # Known Mixer Addresses (Tornado Cash, etc.)
    TORNADO_CASH_ADDRESSES = [
        '0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc',  # 0.1 ETH
        '0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936',  # 1 ETH
        '0x910cbd523d972eb0a6f4cae4618ad62622b39dbf',  # 10 ETH
        '0xa160cdab225685da1d56aa342ad8841c3b53f291',  # 100 ETH
        '0xd4b88df4d29f5cedd6857912842cff3b20c8cfa3',  # DAI 100
        '0xfd8610d20aa15b7b2e3be39b396a1bc3516c7144',  # DAI 1000
        '0xf60dd140cff0706bae9cd734ac3ae76ad9ebc32a',  # DAI 10000
        '0x22aaa7720ddd5388a3c0a3333430953c68f1849b',  # DAI 100000
    ]
    
    # Known Exchange Addresses (for tracking)
    KNOWN_EXCHANGES = {
        '0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be': 'Binance',
        '0xd551234ae421e3bcba99a0da6d736074f22192ff': 'Binance',
        '0x564286362092d8e7936f0549571a803b203aaced': 'Binance',
        '0x0681d8db095565fe8a346fa0277bffde9c0edbbf': 'Binance',
        '0xfe9e8709d3215310075d67e3ed32a380ccf451c8': 'Binance',
        '0x4e9ce36e442e55ecd9025b9a6e0d88485d628a67': 'Binance',
        '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8': 'Binance',
        '0xf977814e90da44bfa03b6295a0616a897441acec': 'Binance',
        '0x001866ae5b3de6caa5a51543fd9fb64f524f5478': 'Binance',
        '0x85b931a32a0725be14285b66f1a22178c672d69b': 'Binance',
        '0x708396f17127c42383e3b9014072679b2f60b82f': 'Binance',
        '0xe0f0cfde7ee664943906f17f7f14342e76a5cec7': 'Binance',
        '0x8f22f2063d253846b53609231ed80fa571bc0c8f': 'Binance',
        '0x28c6c06298d514db089934071355e5743bf21d60': 'Binance',
        '0x21a31ee1afc51d94c2efccaa2092ad1028285549': 'Binance',
        '0xdfd5293d8e347dfe59e90efd55b2956a1343963d': 'Binance',
        '0x56eddb7aa87536c09ccc2793473599fd21a8b17f': 'Binance',
        '0x9696f59e4d72e237be84ffd425dcad154bf96976': 'Binance',
        '0x4d9ff50ef4da947364bb9650892b2554e7be5e2b': 'Binance',
        '0xd88b55467f58af508dbfdc597e8ebd2ad2de49b3': 'Binance',
        '0x7dfe9a368b6cf0c0309b763bb8d16da326e8f46e': 'Binance',
        '0x345d8e3a1f62ee6b1d483890976fd66168e390f2': 'Binance',
        '0xc3c8e0a39769e2308869f7461364ca48155d1d9e': 'Binance',
        '0x2910543af39aba0cd09dbb2d50200b3e800a63d2': 'Kraken',
        '0x0a869d79a7052c7f1b55a8ebabbea3420f0d1e13': 'Kraken',
        '0xe853c56864a2ebe4576a807d26fdc4a0ada51919': 'Kraken',
        '0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0': 'Kraken',
        '0xfa52274dd61e1643d2205169732f29114bc240b3': 'Kraken',
        '0x53d284357ec70ce289d6d64134dfac8e511c8a3d': 'Kraken',
        '0x89e51fa8ca5d66cd220baed62ed01e8951aa7c40': 'Kraken',
        '0xc6bed363b30df7f35b601a5547fe56cd31ec63da': 'Kraken',
        '0x29728d0efd284d85187362faa2d4d76c2cfc2612': 'Kraken',
        '0xae2d4617c862309a3d75a0ffb358c7a5009c673f': 'Kraken',
        '0x43984d578803891dfa9706bdeee6078d80cfc79e': 'Kraken',
        '0x66c57bf505a85a74609d2c83e94aabb26d691e1f': 'Kraken',
        '0xda9dfa130df4de4673b89022ee50ff26f6ea73cf': 'Kraken',
        '0xa83b11093c858c86321fbc4c20fe82cdbd58e09e': 'Kraken',
        '0x6cc5f688a315f3dc28a7781717a9a798a59fda7b': 'Coinbase',
        '0x503828976d22510aad0201ac7ec88293211d23da': 'Coinbase',
        '0xddfabcdc4d8ffc6d5beaf154f18b778f892a0740': 'Coinbase',
        '0x3cd751e6b0078be393132286c442345e5dc49699': 'Coinbase',
        '0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511': 'Coinbase',
        '0xeb2629a2734e272bcc07bda959863f316f4bd4cf': 'Coinbase',
        '0xd688aea8f7d450909ade10c47faa95707b0682d9': 'Coinbase',
        '0x02466e547bfdab679fc49e96bbfc62b9747d997c': 'Coinbase',
        '0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43': 'Coinbase',
        '0x77696bb39917c91a0c3908d577d5e322095425ca': 'Coinbase',
        '0x7c195d981abfdc3ddecd2ca0fed0958430488e34': 'Coinbase',
        '0x95a9bd206ae52c4ba8eecfc93d18eacdd41c88cc': 'Coinbase',
        '0xb739d0895772dbb71a89a3754a160269068f0d45': 'Coinbase',
        '0x4d77a1144dc74f26838b88db677fa1fc857e6c62': 'Coinbase',
        '0x9c2fc4fc75fa2d7eb5ba9147fa7430756654faa9': 'Coinbase',
        '0x4b1a99467a284cc690e3237bc69105956816f762': 'Coinbase',
        '0x2910543af39aba0cd09dbb2d50200b3e800a63d2': 'Coinbase',
        '0xd24400ae8bfebb18ca49be86258a3c749cf46853': 'Coinbase',
        '0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503': 'Coinbase',
        '0x71660c4005ba85c37ccec55d0c4493e66fe775d3': 'Coinbase',
        '0x46340b20830761efd32832a74d7169b29feb9758': 'Coinbase',
        '0x0548f59fee79f8832c299e01dca5c76f034f558e': 'Coinbase',
        '0x0681d8db095565fe8a346fa0277bffde9c0edbbf': 'Coinbase',
        '0xf6874c88757721a02f47592140905c4336dfbc61': 'Coinbase',
        '0x881d4032abe4188e2237efcd27ab435e81fc6bb1': 'Coinbase',
    }
    
    # Risk Score Thresholds
    RISK_SCORE_HIGH = 75
    RISK_SCORE_MEDIUM = 50
    RISK_SCORE_LOW = 25
    
    # Transaction Analysis Settings
    MAX_TRANSACTION_DEPTH = 10  # How many hops to trace
    SIMILAR_ADDRESS_THRESHOLD = 5  # Characters to match for address poisoning detection
    
    # OSINT Settings
    OSINT_CACHE_DURATION = 3600  # 1 hour in seconds
    MAX_OSINT_RESULTS = 100

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}