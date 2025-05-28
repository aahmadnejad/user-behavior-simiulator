# User Behavior Simulator

A comprehensive cross-platform Python package for simulating realistic user behavior including intelligent web browsing with link crawling, dynamic file operations, advanced network file sharing with IP range support, and system monitoring.

## Features

- **🌐 Intelligent Web Browsing**: Automated website visits with deep link crawling and randomized exploration
- **📺 YouTube Integration**: Video watching with duration detection and completion waiting
- **📝 Dynamic File Operations**: Create text files using random content from multiple APIs with configurable save paths
- **🌍 Advanced Network File Sharing**: Share files across network ranges with intelligent retry mechanisms
- **📊 System Monitoring**: Ping network targets with comprehensive logging and IP range support  
- **⏰ Flexible Scheduling**: Random or precise time-based task execution
- **🕐 Active Hours Control**: Restrict activity to specific time ranges (e.g., 9am-5pm)
- **💻 Cross-Platform**: Works seamlessly on Windows, Linux, and macOS

## Installation

### From PyPI (when published)
```bash
pip install user-behavior-simulator
```

### From Source
```bash
git clone https://github.com/username/user-behavior-simulator
cd user-behavior-simulator
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/username/user-behavior-simulator
cd user-behavior-simulator
pip install -e .[dev]
```

## Quick Start

### 1. Create Configuration
```bash
user-behavior-simulator --create-config
```

### 2. Edit Configuration
Edit the generated `config.json` file to customize:
- Websites to visit and crawl
- YouTube videos to watch
- Network IP addresses or ranges
- API endpoints for text generation
- File save locations
- Scheduling preferences

### 3. Run Simulator
```bash
user-behavior-simulator
# or use short command
ubs
```

## Command Line Usage

```bash
# Run with default config
user-behavior-simulator

# Use custom config file
user-behavior-simulator -c my_config.json

# Create default configuration
user-behavior-simulator --create-config

# Show version
user-behavior-simulator --version
```

## Configuration

### Basic Configuration
```json
{
    "websites": [
        "https://www.reddit.com",
        "https://www.github.com",
        "https://stackoverflow.com"
    ],
    "links_per_website": [3, 7],
    "max_crawl_depth": 2,
    "target_ips": [
        "192.168.1.100",
        "192.168.1.101"
    ],
    "save_paths": {
        "text_files": "/home/user/Documents/simulator_texts",
        "downloads": "/home/user/Downloads/simulator_media",
        "ping_logs": "/home/user/Documents/network_logs",
        "received_files": "/home/user/Documents/received_files"
    },
    "active_hours": {
        "enabled": true,
        "start_hour": 9,
        "end_hour": 17
    }
}
```

### Advanced Network Configuration - IP Ranges
```json
{
    "ip_range": {
        "enabled": true,
        "start_ip": "192.168.1.100",
        "end_ip": "192.168.1.200",
        "exclude_ips": [
            "192.168.1.1",
            "192.168.1.2",
            "192.168.1.254",
            "192.168.1.255"
        ]
    },
    "target_ips": [
        "192.168.1.50",
        "192.168.1.51"
    ]
}
```

### Scheduled Tasks
```json
{
    "scheduled_tasks": {
        "enabled": true,
        "tasks": [
            {
                "task": "browse_websites",
                "time": "09:30",
                "enabled": true
            },
            {
                "task": "create_text_files", 
                "time": "10:15",
                "enabled": true
            },
            {
                "task": "watch_youtube",
                "time": "11:00",
                "enabled": true
            },
            {
                "task": "ping_target_ips",
                "time": "12:00",
                "enabled": true
            },
            {
                "task": "download_media",
                "time": "14:30",
                "enabled": true
            },
            {
                "task": "share_files_with_network",
                "time": "15:45",
                "enabled": true
            }
        ]
    }
}
```

## Key Features Explained

### 🌐 Intelligent Web Browsing
- **Deep Link Crawling**: Visits 2-10 additional links per website
- **Multi-Level Exploration**: Configurable crawl depth (1-3 levels)
- **Smart Link Selection**: Filters and selects relevant links within same domain
- **Realistic Timing**: Random delays between page visits (15-90 seconds)

```json
"links_per_website": [3, 7],
"max_crawl_depth": 2,
"explore_time_per_site": [30, 180]
```

### 📁 Flexible File Management
- **Custom Save Paths**: Configure exactly where each file type is saved
- **API-Driven Content**: Fetches random text from quotable.io, lorem ipsum, and JSONPlaceholder
- **Organized Storage**: Separate directories for different file types
- **Cross-Platform Paths**: Handles Windows and Unix path formats automatically

```json
"save_paths": {
    "text_files": "C:\\Users\\username\\Documents\\SimulatorTexts",
    "downloads": "C:\\Users\\username\\Downloads\\SimulatorMedia", 
    "ping_logs": "D:\\Logs\\NetworkPings",
    "received_files": "C:\\Users\\username\\Desktop\\ReceivedFiles"
}
```

### 🌍 Advanced Network Operations
- **IP Range Support**: Target entire network ranges instead of individual IPs
- **Smart Availability Checking**: Pings IPs before attempting file transfers
- **Robust Retry Logic**: 3 attempts per IP with exponential backoff
- **Fallback Mechanisms**: Falls back to individual IPs if range fails
- **Network Device Handling**: Automatically excludes routers, switches, and non-responsive devices

```json
"ip_range": {
    "enabled": true,
    "start_ip": "192.168.1.100",
    "end_ip": "192.168.1.200", 
    "exclude_ips": ["192.168.1.1", "192.168.1.254"]
}
```

### ⏰ Sophisticated Scheduling
- **Active Hours**: Restrict operations to business hours or specific time windows
- **Precise Scheduling**: Execute tasks at exact times (e.g., 09:30, 14:45)
- **Random Mode**: Natural behavior with random intervals
- **Mixed Scheduling**: Combine scheduled and random behaviors

## Network Setup

### Firewall Configuration

#### Windows 10/11
1. **Open Windows Defender Firewall**:
   - Press `Win + R`, type `wf.msc`, press Enter
   
2. **Create Inbound Rule**:
   - Click "Inbound Rules" → "New Rule"
   - Select "Port" → Next
   - Select "TCP" → "Specific local ports" → Enter `8888`
   - Select "Allow the connection" → Next
   - Check all profiles → Next
   - Name: "User Behavior Simulator" → Finish

3. **Create Outbound Rule** (repeat same steps for Outbound Rules)

#### Linux (Ubuntu/Debian)
```bash
sudo ufw allow 8888/tcp
sudo ufw enable
```

#### Linux (CentOS/RHEL/Fedora)
```bash
sudo firewall-cmd --permanent --add-port=8888/tcp
sudo firewall-cmd --reload
```

### Network Discovery
```bash
# Find IP addresses
# Windows
ipconfig

# Linux/Mac
ip addr show
hostname -I
```

### Testing Network Connectivity
```bash
# Test ping between machines
ping 192.168.1.101

# Test port connectivity
# Windows
telnet 192.168.1.101 8888

# Linux
nc -zv 192.168.1.101 8888
```

## API Integration

The simulator integrates with multiple APIs for dynamic content generation:

### Supported APIs
- **Quotable API**: Random inspirational quotes with authors
- **Lorem Ipsum API**: Placeholder text in paragraphs
- **JSONPlaceholder**: Sample JSON posts and content

### Custom API Configuration
```json
"text_apis": [
    "https://api.quotable.io/random?minLength=100",
    "https://loremipsum.io/api",
    "https://jsonplaceholder.typicode.com/posts",
    "https://your-custom-api.com/random-text"
]
```

## Programming Interface

### Basic Usage
```python
from user_behavior_simulator import UserBehaviorSimulator

# Create simulator with default config
simulator = UserBehaviorSimulator()

# Create with custom config
simulator = UserBehaviorSimulator('my_config.json')

# Start simulation
simulator.start()

# Stop simulation
simulator.stop()
```

### Advanced Integration
```python
from user_behavior_simulator import UserBehaviorSimulator

class CustomSimulator(UserBehaviorSimulator):
    def custom_task(self):
        print("Running custom network scan")
        # Your custom logic here
        
    def custom_file_processing(self):
        print("Processing files with custom logic")
        # Your file processing logic
    
    def execute_task_by_name(self, task_name):
        if task_name == "custom_task":
            self.custom_task()
        elif task_name == "custom_processing":
            self.custom_file_processing()
        else:
            super().execute_task_by_name(task_name)

# Use custom simulator
simulator = CustomSimulator()
simulator.start()
```

### Configuration Management
```python
import json

# Load and modify config programmatically
with open('config.json', 'r') as f:
    config = json.load(f)

# Enable IP range for current network
config['ip_range']['enabled'] = True
config['ip_range']['start_ip'] = '192.168.1.100'
config['ip_range']['end_ip'] = '192.168.1.150'

# Save modified config
with open('custom_config.json', 'w') as f:
    json.dump(config, f, indent=4)

# Use modified config
simulator = UserBehaviorSimulator('custom_config.json')
```

## Task Types

1. **browse_websites**: Visit configured websites and crawl internal links
2. **watch_youtube**: Play YouTube videos and wait for completion
3. **create_text_files**: Generate text files using API content in configured directories
4. **download_media**: Download files from configured URLs to specified locations
5. **share_files_with_network**: Send files to network computers with retry logic
6. **ping_target_ips**: Ping network targets (ranges or individual IPs) and log results

## Configuration Examples

### Home Network Setup
```json
{
    "ip_range": {
        "enabled": true,
        "start_ip": "192.168.1.10",
        "end_ip": "192.168.1.50",
        "exclude_ips": ["192.168.1.1", "192.168.1.254"]
    },
    "save_paths": {
        "text_files": "/home/user/Documents/HomeSimulator",
        "downloads": "/home/user/Downloads/SimulatorMedia"
    },
    "links_per_website": [2, 5],
    "active_hours": {
        "enabled": true,
        "start_hour": 8,
        "end_hour": 22
    }
}
```

### Corporate Network Setup
```json
{
    "ip_range": {
        "enabled": true,
        "start_ip": "10.0.1.100",
        "end_ip": "10.0.1.200", 
        "exclude_ips": [
            "10.0.1.1",
            "10.0.1.10",
            "10.0.1.254"
        ]
    },
    "save_paths": {
        "text_files": "C:\\CorporateSimulator\\TextFiles",
        "downloads": "C:\\CorporateSimulator\\Downloads",
        "ping_logs": "C:\\CorporateSimulator\\Logs"
    },
    "scheduled_tasks": {
        "enabled": true,
        "tasks": [
            {"task": "browse_websites", "time": "09:00", "enabled": true},
            {"task": "ping_target_ips", "time": "12:00", "enabled": true},
            {"task": "share_files_with_network", "time": "15:00", "enabled": true}
        ]
    },
    "active_hours": {
        "enabled": true,
        "start_hour": 9,
        "end_hour": 17
    }
}
```

## Security Considerations

### Network Security
- File sharing creates an open service on your network
- Only use on trusted networks  
- Consider firewall rules for production environments
- Files are transferred without encryption
- Monitor network traffic as needed

### Access Control
- Configure `exclude_ips` to avoid sensitive network devices
- Use `active_hours` to limit when simulation runs
- Regular monitoring of generated files and network activity

### Data Privacy
- Text files contain random API content - review APIs used
- Network transfers are logged - consider log retention policies
- File paths are configurable - ensure appropriate permissions

## Troubleshooting

### Common Issues

#### IP Range Not Working
- Check network connectivity: `ping [start_ip]`
- Verify IP range is within same subnet
- Ensure excluded IPs include all network infrastructure
- Test with smaller range first

#### File Transfer Failures
```bash
# Check if port is open
# Windows
netstat -an | findstr :8888

# Linux  
ss -tuln | grep :8888

# Test connectivity
telnet [target_ip] 8888
```

#### Permission Issues
- Ensure write permissions to configured save paths
- Run as administrator on Windows if needed
- Check firewall allows Python network access
- Verify target directories exist and are writable

#### API Rate Limiting
- APIs may have rate limits - simulator handles gracefully
- Falls back to generated content if APIs fail
- Consider adding delays between API calls in heavy usage

#### Network Discovery Problems
```bash
# Scan network for active IPs
# Linux
nmap -sn 192.168.1.0/24

# Windows (if nmap installed)
nmap -sn 192.168.1.1-254
```

### Performance Optimization

#### Large IP Ranges
- System samples max 10 IPs for availability checking
- Use targeted ranges instead of entire subnets
- Consider network bandwidth limitations
- Monitor system resources during operation

#### File Operations
- Configure appropriate `task_wait_minutes` for your system
- Monitor disk space usage
- Regular cleanup of generated files
- Use SSD storage for better performance

### Debug Mode
Enable verbose logging by modifying the simulator:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

simulator = UserBehaviorSimulator()
simulator.start()
```

## Development

### Project Structure
```
user_behavior_simulator/
├── __init__.py          # Package initialization
├── main.py              # Command-line interface  
├── simulator.py         # Core simulation logic
└── config.json          # Default configuration
```

### Building Package
```bash
python -m build
twine check dist/*
```

### Running Tests
```bash
python -m pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add comprehensive tests
5. Update documentation
6. Submit a pull request

## License

MIT License - see LICENSE file for details.


## Support

For issues, feature requests, or questions:
- GitHub Issues: [Create an issue](https://github.com/aahmadnejad/user-behavior-simiulator/issues)
- Documentation: [Full documentation](https://github.com/aahmadnejad/user-behavior-simiulator/wiki)
- Email: amirhahm@yorku.ca

## Acknowledgments

- This is a project with BCCC Lab @ York University
- Thanks to the open-source APIs used for content generation
- Cross-platform compatibility testing contributors
- Network security review contributors