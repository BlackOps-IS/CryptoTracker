# 🛡️ CryptoTracker - Advanced Blockchain Forensics & Victim Support System

![CryptoTracker Banner](https://img.shields.io/badge/CryptoTracker-Blockchain%20Forensics-00d4ff?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**CryptoTracker** is a comprehensive blockchain forensics and victim support system designed to help victims of cryptocurrency theft track stolen funds, gather intelligence, and maximize recovery chances. Built by **BlackOps-IS**, this tool combines advanced blockchain analysis, OSINT collection, and professional recovery assistance.

---

## 🎯 Key Features

### 🔍 Advanced Address Tracking
- **Real-time transaction monitoring** across Ethereum and other EVM chains
- **Address poisoning detection** - Identify suspicious addresses with similar patterns
- **Mixer detection** - Track interactions with Tornado Cash and other privacy protocols
- **Exchange identification** - Detect when funds hit known exchanges (critical for recovery)
- **Risk scoring** - Automated risk assessment based on transaction patterns

### 🕵️ OSINT Intelligence Collection
- **On-chain intelligence** - First seen, last seen, transaction patterns
- **Public label aggregation** - Etherscan labels, known entities
- **Threat intelligence** - Check against scam databases and blacklists
- **Social mention scanning** - Find public references to addresses
- **Comprehensive reporting** - Generate detailed intelligence reports

### 🆘 Recovery Assistance
- **Automated recovery plans** - Step-by-step action plans based on incident details
- **Whitehat negotiation templates** - Professional on-chain messages
- **Law enforcement packages** - Complete evidence bundles for authorities
- **Exchange reporting templates** - Ready-to-send reports for exchanges
- **Recovery probability estimation** - Realistic assessment of recovery chances

### 📚 Prevention & Education
- **Address verification best practices**
- **Transaction safety guidelines**
- **Security recommendations**
- **Common scam awareness**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 20.x (for frontend dependencies)
- Etherscan API key (free tier available)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/BlackOps-IS/CryptoTracker.git
cd CryptoTracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Run the application**
```bash
python app.py
```

5. **Access the dashboard**
```
Open your browser to: http://localhost:5000
```

---

## 📖 Usage Guide

### Analyzing an Address

1. Navigate to the **Address Tracker** section
2. Enter the Ethereum address you want to analyze
3. Click **Analyze** to get:
   - Current balance
   - Risk assessment
   - Transaction patterns
   - Address poisoning detection
   - Mixer usage detection
   - Exchange interactions

### Gathering OSINT

1. Go to the **OSINT Intelligence** section
2. Enter the address for investigation
3. Click **Gather OSINT** to collect:
   - On-chain intelligence
   - Public labels and tags
   - Threat intelligence
   - Risk factors
   - Comprehensive report

### Creating a Recovery Plan

1. Navigate to **Recovery Assistance**
2. Fill in the incident details:
   - Victim address
   - Attacker address
   - Amount stolen
   - Token type
   - Incident date
3. Click **Generate Recovery Plan** to receive:
   - Immediate action items (1-4 hours)
   - Short-term actions (24-48 hours)
   - Long-term strategy
   - Recovery probability assessment
   - Estimated timeline

### Quick Actions

- **Whitehat Message**: Generate professional negotiation message
- **Law Enforcement Package**: Create evidence bundle for authorities
- **Exchange Report**: Generate report template for exchanges

---

## 🏗️ Architecture

### Backend Components

```
src/
├── blockchain/          # Blockchain analysis engine
│   └── analyzer.py      # Transaction tracking, pattern analysis
├── osint/              # OSINT collection system
│   └── collector.py    # Intelligence gathering, threat detection
├── recovery/           # Recovery assistance
│   └── assistant.py    # Recovery plans, templates, strategies
└── utils/              # Utility functions
    └── helpers.py      # Formatting, validation, helpers
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Analyze cryptocurrency address |
| `/api/trace` | POST | Trace fund flow from address |
| `/api/transaction` | POST | Analyze specific transaction |
| `/api/osint` | POST | Gather OSINT intelligence |
| `/api/osint/report` | POST | Generate OSINT report |
| `/api/recovery/plan` | POST | Generate recovery plan |
| `/api/recovery/whitehat` | POST | Generate whitehat message |
| `/api/recovery/law-enforcement` | POST | Generate LE package |
| `/api/recovery/exchange-report` | POST | Generate exchange report |
| `/api/prevention` | GET | Get prevention tips |
| `/api/export` | POST | Export analysis report |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Blockchain API Keys
ETHERSCAN_API_KEY=your_etherscan_api_key
BSCSCAN_API_KEY=your_bscscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key

# Web3 Provider URLs
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-api-key
BSC_RPC_URL=https://bsc-dataseed.binance.org/
POLYGON_RPC_URL=https://polygon-rpc.com/

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///cryptotracker.db

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### Getting API Keys

1. **Etherscan API Key** (Required)
   - Visit: https://etherscan.io/apis
   - Sign up for free account
   - Generate API key

2. **Alchemy RPC** (Optional, for better performance)
   - Visit: https://www.alchemy.com/
   - Create free account
   - Get Ethereum RPC URL

---

## 💡 Real-World Use Cases

### Case Study: Address Poisoning Attack

**Scenario**: User lost $50M USDT to address poisoning attack

**How CryptoTracker Helps**:
1. **Detection**: Identifies similar addresses in transaction history
2. **Analysis**: Tracks where funds went (mixer, exchange, etc.)
3. **Recovery Plan**: Generates immediate action items:
   - Contact Tether to freeze USDT
   - Alert exchanges where funds deposited
   - File police report with evidence
   - Send whitehat negotiation message
4. **Evidence**: Creates law enforcement package with:
   - Complete transaction timeline
   - Blockchain analysis
   - OSINT intelligence
   - Recommended actions

**Result**: Maximizes recovery chances through rapid, coordinated response

---

## 🛡️ Security & Privacy

### What We Track
- ✅ Public blockchain data only
- ✅ Publicly available information
- ✅ Known exchange addresses
- ✅ Reported scam addresses

### What We DON'T Track
- ❌ Private keys or seed phrases
- ❌ Personal information without consent
- ❌ Data behind authentication walls
- ❌ Anything illegal or unethical

### Legal Compliance
- All data collection is from public sources
- Complies with GDPR, CCPA, and other privacy laws
- No unauthorized access to private systems
- Respects API terms of service

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with details
2. **Suggest Features**: Share your ideas
3. **Submit PRs**: Follow our coding standards
4. **Improve Docs**: Help us make documentation better

### Development Setup

```bash
# Clone the repo
git clone https://github.com/BlackOps-IS/CryptoTracker.git
cd CryptoTracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run the app
python app.py
```

---

## 📊 Roadmap

### Phase 1: Core Features ✅
- [x] Address tracking and analysis
- [x] OSINT collection
- [x] Recovery assistance
- [x] Web interface

### Phase 2: Enhanced Features 🚧
- [ ] Multi-chain support (BSC, Polygon, Arbitrum)
- [ ] Real-time monitoring and alerts
- [ ] Advanced graph visualization
- [ ] Machine learning for pattern detection

### Phase 3: Enterprise Features 📋
- [ ] API for integration
- [ ] Team collaboration features
- [ ] Advanced reporting
- [ ] Custom threat intelligence feeds

---

## 🎓 Educational Resources

### Understanding Address Poisoning
Address poisoning is a sophisticated attack where scammers:
1. Generate addresses similar to your legitimate addresses
2. Send small "dust" transactions to your wallet
3. Hope you copy the wrong address from your history
4. Steal large amounts when you send to the poisoned address

**Prevention**: Always verify the FULL address, not just first/last characters

### Mixer Detection Importance
When funds go through mixers like Tornado Cash:
- Transaction trail becomes harder to follow
- Recovery becomes more complex
- But NOT impossible - patterns can still be detected

**CryptoTracker helps**: Identifies mixer usage and provides strategies

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/BlackOps-IS/CryptoTracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BlackOps-IS/CryptoTracker/discussions)
- **Email**: support@blackops-is.com

---

## ⚖️ Legal Disclaimer

**IMPORTANT**: CryptoTracker is provided for educational and legitimate recovery purposes only.

- ✅ Use for recovering your own stolen funds
- ✅ Use for legitimate investigations
- ✅ Use for educational purposes
- ❌ Do NOT use for illegal activities
- ❌ Do NOT use to harass or stalk individuals
- ❌ Do NOT use to violate privacy laws

**No Guarantees**: While we provide tools to maximize recovery chances, we cannot guarantee fund recovery. Cryptocurrency transactions are irreversible, and recovery depends on many factors outside our control.

**Not Financial Advice**: This tool does not provide financial, legal, or investment advice. Consult with professionals for your specific situation.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **Etherscan** - For blockchain data API
- **Web3.py** - For Ethereum interaction
- **Flask** - For web framework
- **Community** - For feedback and support

---

## 🌟 Star History

If you find CryptoTracker useful, please consider giving it a star! ⭐

---

**Built with 💪 by BlackOps-IS**

*Putting the fear of BlackOps into crypto criminals, one recovery at a time.*

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/images/dashboard.png)

### Address Analysis
![Analysis](docs/images/analysis.png)

### Recovery Plan
![Recovery](docs/images/recovery.png)

---

**Remember**: The best defense is prevention. Always verify addresses, use hardware wallets, and stay informed about the latest scams.

**Let's make crypto safer together! 🛡️**