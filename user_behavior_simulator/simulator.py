import os
import sys
import time
import random
import json
import socket
import threading
import subprocess
import platform
from datetime import datetime, timedelta
import webbrowser
import requests
from urllib.parse import urlparse
import tempfile
import shutil
import re

class UserBehaviorSimulator:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.is_running = False
        self.threads = []
        
    def load_config(self, config_file):
        default_config = {
            "websites": [
                "https://www.amazon.ca",
                "https://www.wikipedia.org",
                "https://www.google.com",
                "https://www.stackoverflow.com",
                "https://www.github.com",
                "https://www.reddit.com",
                "https://www.news.ycombinator.com",
                "https://www.yorku.ca/research/bccc/",
                "https://www.yorku.ca/"
            ],
            "youtube_videos": [
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
                "https://www.youtube.com/watch?v=oHg5SJYRHA0",
                "https://www.youtube.com/watch?v=7N_NNVeKat8"
            ],
            "media_urls": [
                "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                "https://file-examples.com/storage/fe6e2f36b3d06aff0bf72da/2017/10/file_example_JPG_100kB.jpg"
            ],
            "target_ips": [
                "192.168.1.100",
                "192.168.1.101"
            ],
            "ip_range": {
                "enabled": True,
                "network": "192.168.1.0",
                "subnet_mask": "255.255.255.0",
                "start_ip": "192.168.1.50",
                "end_ip": "192.168.1.200",
                "exclude_ips": [
                    "192.168.1.1",
                    "192.168.1.61",
                    "192.168.1.54",
                    "192.168.1.53",
                    "192.168.1.255"
                ]
            },
            "text_apis": [
                "https://api.quotable.io/random?minLength=100",
                "https://loremipsum.io/api",
                "https://jsonplaceholder.typicode.com/posts"
            ],
            "file_share_port": 8888,
            "daily_sessions": 3,
            "session_duration_minutes": [50, 120],
            "explore_time_per_site": [2, 10],
            "files_to_create_per_day": 5,
            "task_wait_minutes": [0, 5],
            "ping_count": 4,
            "video_completion_check_interval": 30,
            "links_per_website": [2, 6],
            "max_crawl_depth": 2,
            "save_paths": {
                "text_files": "",
                "downloads": "",
                "ping_logs": "",
                "received_files": ""
            },
            "active_hours": {
                "enabled": True,
                "start_hour": 9,
                "end_hour": 17
            },
            "scheduled_tasks": {
                "enabled": False,
                "tasks": [
                    {
                        "task": "browse_websites",
                        "time": "09:30",
                        "enabled": True
                    },
                    {
                        "task": "create_text_files",
                        "time": "10:15",
                        "enabled": True
                    },
                    {
                        "task": "watch_youtube",
                        "time": "11:00",
                        "enabled": True
                    },
                    {
                        "task": "ping_target_ips",
                        "time": "12:00",
                        "enabled": True
                    },
                    {
                        "task": "download_media",
                        "time": "14:30",
                        "enabled": True
                    },
                    {
                        "task": "share_files_with_network",
                        "time": "15:45",
                        "enabled": True
                    }
                ]
            }
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                default_config.update(loaded_config)
            except:
                pass
        else:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
                
        return default_config
    
    def is_within_active_hours(self):
        if not self.config['active_hours']['enabled']:
            return True
            
        current_hour = datetime.now().hour
        start_hour = self.config['active_hours']['start_hour']
        end_hour = self.config['active_hours']['end_hour']
        
        if start_hour <= end_hour:
            return start_hour <= current_hour < end_hour
        else:
            return current_hour >= start_hour or current_hour < end_hour
    
    def wait_for_active_hours(self):
        while not self.is_within_active_hours() and self.is_running:
            time.sleep(60)
    
    def should_run_scheduled_task(self, task_config):
        if not task_config['enabled']:
            return False
            
        current_time = datetime.now().strftime("%H:%M")
        target_time = task_config['time']
        
        current_datetime = datetime.strptime(current_time, "%H:%M")
        target_datetime = datetime.strptime(target_time, "%H:%M")
        
        time_diff = abs((current_datetime - target_datetime).total_seconds())
        
        return time_diff <= 60
    
    def get_next_scheduled_task(self):
        if not self.config['scheduled_tasks']['enabled']:
            return None
            
        current_time = datetime.now().strftime("%H:%M")
        current_datetime = datetime.strptime(current_time, "%H:%M")
        
        upcoming_tasks = []
        
        for task_config in self.config['scheduled_tasks']['tasks']:
            if not task_config['enabled']:
                continue
                
            target_datetime = datetime.strptime(task_config['time'], "%H:%M")
            
            if target_datetime > current_datetime:
                time_diff = (target_datetime - current_datetime).total_seconds()
                upcoming_tasks.append((time_diff, task_config))
            else:
                time_diff = (target_datetime + timedelta(days=1) - current_datetime).total_seconds()
                upcoming_tasks.append((time_diff, task_config))
        
        if upcoming_tasks:
            upcoming_tasks.sort(key=lambda x: x[0])
            return upcoming_tasks[0]
        
        return None
    
    def wait_between_tasks(self):
        wait_time = random.randint(*self.config['task_wait_minutes']) * 60
        time.sleep(wait_time)
    
    def get_random_text_from_api(self):
        apis = self.config['text_apis']
        
        for _ in range(3):
            try:
                api_url = random.choice(apis)
                
                if "quotable.io" in api_url:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        return f"Quote: {data['content']}\nAuthor: {data['author']}"
                
                elif "loremipsum.io" in api_url:
                    response = requests.get(f"{api_url}?type=paragraph&amount=3", timeout=10)
                    if response.status_code == 200:
                        return response.text
                
                elif "jsonplaceholder.typicode.com" in api_url:
                    post_id = random.randint(1, 100)
                    response = requests.get(f"{api_url}/{post_id}", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        return f"Title: {data['title']}\n\nContent: {data['body']}"
                
                else:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        return response.text[:1000]
                        
            except:
                continue
        
        return self.generate_random_text()
    
    def get_save_path(self, path_type):
        configured_path = self.config['save_paths'].get(path_type, "")
        
        if configured_path and os.path.exists(configured_path):
            return configured_path
        
        if path_type == "text_files":
            return random.choice([self.get_desktop_path(), self.get_documents_path()])
        elif path_type == "downloads":
            return os.path.join(self.get_desktop_path(), "downloads")
        elif path_type == "ping_logs":
            return os.path.join(self.get_desktop_path(), "ping_logs")
        elif path_type == "received_files":
            return os.path.join(self.get_desktop_path(), "received")
        else:
            return self.get_desktop_path()
    
    def extract_links_from_page(self, url):
        try:
            import re
            from urllib.parse import urljoin, urlparse
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return []
            
            content = response.text
            base_domain = urlparse(url).netloc
            
            link_patterns = [
                r'href=[\'"]([^\'"]*)[\'"]',
                r'<a[^>]+href=[\'"]([^\'"]*)[\'"]'
            ]
            
            links = []
            for pattern in link_patterns:
                found_links = re.findall(pattern, content, re.IGNORECASE)
                links.extend(found_links)
            
            valid_links = []
            for link in links:
                if not link or link.startswith('#') or link.startswith('javascript:'):
                    continue
                
                if link.startswith('mailto:') or link.startswith('tel:'):
                    continue
                
                full_url = urljoin(url, link)
                parsed_url = urlparse(full_url)
                
                if parsed_url.netloc == base_domain and parsed_url.scheme in ['http', 'https']:
                    if full_url not in valid_links and full_url != url:
                        valid_links.append(full_url)
                
                if len(valid_links) >= 20:
                    break
            
            return valid_links[:20]
            
        except Exception:
            return []
    
    def browse_websites(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting website browsing task")
        websites = self.config['websites']
        
        for _ in range(random.randint(1, len(websites))):
            main_site = random.choice(websites)
            
            try:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening main site: {main_site}")
                webbrowser.open(main_site)
                explore_time = random.randint(*self.config['explore_time_per_site'])
                time.sleep(explore_time)
                
                links_to_visit = random.randint(*self.config['links_per_website'])
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Finding {links_to_visit} additional links from {main_site}")
                
                extracted_links = self.extract_links_from_page(main_site)
                
                if extracted_links:
                    selected_links = random.sample(extracted_links, min(links_to_visit, len(extracted_links)))
                    
                    for link in selected_links:
                        try:
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening additional link: {link}")
                            webbrowser.open(link)
                            
                            link_explore_time = random.randint(15, 90)
                            time.sleep(link_explore_time)
                            
                            if self.config['max_crawl_depth'] > 1:
                                sub_links = self.extract_links_from_page(link)
                                if sub_links:
                                    sub_link = random.choice(sub_links)
                                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening sub-link: {sub_link}")
                                    webbrowser.open(sub_link)
                                    time.sleep(random.randint(10, 60))
                                    
                        except Exception:
                            pass
                        
                        time.sleep(random.randint(5, 15))
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] No additional links found for {main_site}")
                    
            except Exception:
                pass
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed website browsing task")
        if not self.config['scheduled_tasks']['enabled']:
            self.wait_between_tasks()
    
    def get_youtube_video_duration(self, video_url):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['powershell', '-Command', 
                    f'(Invoke-WebRequest -Uri "{video_url}").Content'], 
                    capture_output=True, text=True, timeout=30)
                content = result.stdout
            else:
                result = subprocess.run(['curl', '-s', video_url], 
                    capture_output=True, text=True, timeout=30)
                content = result.stdout
            
            duration_match = re.search(r'"approxDurationMs":"(\d+)"', content)
            if duration_match:
                return int(duration_match.group(1)) / 1000
            
            length_match = re.search(r'"lengthSeconds":"(\d+)"', content)
            if length_match:
                return int(length_match.group(1))
                
        except:
            pass
        
        return random.randint(180, 600)
    
    def watch_youtube(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting YouTube watching task")
        videos = self.config['youtube_videos']
        if videos:
            video = random.choice(videos)
            try:
                duration = self.get_youtube_video_duration(video)
                webbrowser.open(video)
                
                check_interval = self.config['video_completion_check_interval']
                elapsed = 0
                
                while elapsed < duration:
                    time.sleep(min(check_interval, duration - elapsed))
                    elapsed += check_interval
                    
            except:
                time.sleep(random.randint(180, 600))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed YouTube watching task")
        if not self.config['scheduled_tasks']['enabled']:
            self.wait_between_tasks()
    
    def create_text_files(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting text file creation task")
        save_path = self.get_save_path("text_files")
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        for i in range(self.config['files_to_create_per_day']):
            filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.txt"
            content = self.get_random_text_from_api()
            
            filepath = os.path.join(save_path, filename)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Created file: {filepath}")
                time.sleep(random.randint(10, 30))
            except:
                pass
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed text file creation task")
        if not self.config['scheduled_tasks']['enabled']:
            self.wait_between_tasks()
    
    def ping_target_ips(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting ping task")
        
        target_ips = self.generate_ip_range()
        ping_count = self.config['ping_count']
        
        if self.config['ip_range']['enabled']:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Pinging IP range with {len(target_ips)} addresses")
            target_ips = random.sample(target_ips, min(10, len(target_ips)))
        
        log_path = self.get_save_path("ping_logs")
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        
        for ip in target_ips:
            try:
                if platform.system() == "Windows":
                    cmd = ['ping', '-n', str(ping_count), ip]
                else:
                    cmd = ['ping', '-c', str(ping_count), ip]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                log_file = os.path.join(log_path, f"ping_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                with open(log_file, 'w') as f:
                    f.write(f"Ping results for {ip}:\n")
                    f.write(f"Return code: {result.returncode}\n")
                    f.write("STDOUT:\n")
                    f.write(result.stdout)
                    if result.stderr:
                        f.write("\nSTDERR:\n")
                        f.write(result.stderr)
                
                status = "SUCCESS" if result.returncode == 0 else "FAILED"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Ping {ip}: {status}")
                time.sleep(random.randint(5, 15))
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error pinging {ip}: {e}")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed ping task")
        if not self.config['scheduled_tasks']['enabled']:
            self.wait_between_tasks()
    
    def get_desktop_path(self):
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if os.path.exists(desktop):
                return desktop
            return os.path.expanduser("~")
    
    def get_documents_path(self):
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Documents")
        else:
            return os.path.join(os.path.expanduser("~"), "Documents")
    
    def generate_random_text(self):
        sentences = [
            "This is a sample document created automatically.",
            "The weather today is quite pleasant for outdoor activities.",
            "Technology continues to evolve at an unprecedented pace.",
            "Many people enjoy reading books in their spare time.",
            "Coffee shops have become popular places for remote work.",
            "Exercise is important for maintaining good health.",
            "Travel broadens one's perspective on different cultures.",
            "Music has the power to evoke strong emotions.",
            "Learning new skills is a lifelong journey.",
            "Nature provides a peaceful escape from city life."
        ]
        
        num_sentences = random.randint(3, 8)
        selected_sentences = random.sample(sentences, num_sentences)
        return "\n".join(selected_sentences)
    
    def download_media(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting media download task")
        media_urls = self.config['media_urls']
        download_path = self.get_save_path("downloads")
        
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        for url in media_urls:
            try:
                response = requests.get(url, stream=True, timeout=60)
                if response.status_code == 200:
                    filename = os.path.basename(urlparse(url).path)
                    if not filename:
                        filename = f"media_{int(time.time())}"
                    
                    filepath = os.path.join(download_path, filename)
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloaded: {filepath}")
                    time.sleep(random.randint(5, 15))
            except:
                pass
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed media download task")
        if not self.config['scheduled_tasks']['enabled']:
            self.wait_between_tasks()
    
    def generate_ip_range(self):
        if not self.config['ip_range']['enabled']:
            return self.config['target_ips']
        
        try:
            import ipaddress
            
            start_ip = self.config['ip_range']['start_ip']
            end_ip = self.config['ip_range']['end_ip']
            exclude_ips = set(self.config['ip_range']['exclude_ips'])
            
            start = ipaddress.IPv4Address(start_ip)
            end = ipaddress.IPv4Address(end_ip)
            
            ip_list = []
            current = start
            
            while current <= end:
                ip_str = str(current)
                if ip_str not in exclude_ips:
                    ip_list.append(ip_str)
                current += 1
            
            return ip_list
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error generating IP range: {e}")
            return self.config['target_ips']
    
    def ping_ip_to_check_availability(self, ip):
        try:
            if platform.system() == "Windows":
                cmd = ['ping', '-n', '1', '-w', '1000', ip]
            else:
                cmd = ['ping', '-c', '1', '-W', '1', ip]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def send_file_to_ip_with_retry(self, ip, filepath, max_retries=3):
        for attempt in range(max_retries):
            try:
                if not self.ping_ip_to_check_availability(ip):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] IP {ip} not reachable, skipping")
                    return False
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((ip, self.config['file_share_port']))
                
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)
                
                header = f"{filename}|{filesize}"
                sock.send(header.encode())
                
                time.sleep(0.1)
                
                with open(filepath, 'rb') as f:
                    bytes_sent = 0
                    while bytes_sent < filesize:
                        data = f.read(4096)
                        if not data:
                            break
                        sock.send(data)
                        bytes_sent += len(data)
                
                sock.close()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Successfully sent {filename} to {ip}")
                return True
                
            except socket.timeout:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Timeout sending to {ip}, attempt {attempt + 1}/{max_retries}")
            except ConnectionRefusedError:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection refused by {ip}, attempt {attempt + 1}/{max_retries}")
            except OSError as e:
                if "Network is unreachable" in str(e) or "No route to host" in str(e):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Network unreachable to {ip}")
                    return False
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Network error to {ip}: {e}, attempt {attempt + 1}/{max_retries}")
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error sending to {ip}: {e}, attempt {attempt + 1}/{max_retries}")
            
            if attempt < max_retries - 1:
                time.sleep(random.randint(2, 5))
        
        return False
    
    def share_files_with_network(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting file sharing task")
        
        target_ips = self.generate_ip_range()
        
        if self.config['ip_range']['enabled']:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Generated {len(target_ips)} IPs from range")
            available_ips = []
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking IP availability...")
            for ip in random.sample(target_ips, min(10, len(target_ips))):
                if self.ping_ip_to_check_availability(ip):
                    available_ips.append(ip)
            
            if available_ips:
                target_ips = available_ips
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(available_ips)} available IPs")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No IPs responding, using configured targets")
                target_ips = self.config['target_ips']
        
        text_files_path = self.get_save_path("text_files")
        desktop_path = self.get_desktop_path()
        
        search_paths = [text_files_path, desktop_path]
        
        try:
            all_files = []
            for search_path in search_paths:
                if os.path.exists(search_path):
                    files = [os.path.join(search_path, f) for f in os.listdir(search_path) if f.endswith('.txt')]
                    all_files.extend(files)
            
            if all_files:
                file_to_share = random.choice(all_files)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sharing file: {os.path.basename(file_to_share)}")
                
                successful_transfers = 0
                max_attempts = min(5, len(target_ips))
                
                selected_ips = random.sample(target_ips, min(max_attempts, len(target_ips)))
                
                for ip in selected_ips:
                    success = self.send_file_to_ip_with_retry(ip, file_to_share)
                    if success:
                        successful_transfers += 1
                        if successful_transfers >= 2:
                            break
                    time.sleep(random.randint(1, 3))
                
                if successful_transfers == 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] File sharing failed to all targets")
                    
                    fallback_ips = [ip for ip in self.config['target_ips'] if ip not in selected_ips]
                    if fallback_ips:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Trying fallback IPs...")
                        for fallback_ip in fallback_ips[:2]:
                            if self.send_file_to_ip_with_retry(fallback_ip, file_to_share):
                                successful_transfers += 1
                                break
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Successfully shared to {successful_transfers} targets")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No files available to share")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in file sharing: {e}")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed file sharing task")
        if not self.config['scheduled_tasks']['enabled']:
            self.wait_between_tasks()
    
    def start_file_receiver(self):
        def receiver():
            try:
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_sock.bind(('0.0.0.0', self.config['file_share_port']))
                server_sock.listen(5)
                server_sock.settimeout(1)
                
                while self.is_running:
                    try:
                        client_sock, addr = server_sock.accept()
                        client_sock.settimeout(30)
                        
                        header = client_sock.recv(1024).decode()
                        filename, filesize = header.split('|')
                        filesize = int(filesize)
                        
                        received_path = os.path.join(self.get_save_path("received_files"))
                        if not os.path.exists(received_path):
                            os.makedirs(received_path)
                        
                        filepath = os.path.join(received_path, filename)
                        
                        with open(filepath, 'wb') as f:
                            received = 0
                            while received < filesize:
                                data = client_sock.recv(min(4096, filesize - received))
                                if not data:
                                    break
                                f.write(data)
                                received += len(data)
                        
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Received file: {filename}")
                        client_sock.close()
                    except socket.timeout:
                        continue
                    except:
                        pass
                
                server_sock.close()
            except:
                pass
        
        thread = threading.Thread(target=receiver)
        thread.daemon = True
        return thread
    
    def execute_task_by_name(self, task_name):
        task_methods = {
            'browse_websites': self.browse_websites,
            'watch_youtube': self.watch_youtube,
            'create_text_files': self.create_text_files,
            'download_media': self.download_media,
            'share_files_with_network': self.share_files_with_network,
            'ping_target_ips': self.ping_target_ips
        }
        
        if task_name in task_methods:
            try:
                task_methods[task_name]()
            except:
                pass
    
    def scheduled_behavior_cycle(self):
        print("Running in scheduled mode")
        while self.is_running:
            self.wait_for_active_hours()
            
            if not self.is_running:
                break
            
            next_task_info = self.get_next_scheduled_task()
            
            if next_task_info:
                wait_seconds, task_config = next_task_info
                
                if wait_seconds > 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Next task '{task_config['task']}' scheduled for {task_config['time']}, waiting {int(wait_seconds/60)} minutes")
                    
                    while wait_seconds > 0 and self.is_running:
                        sleep_time = min(60, wait_seconds)
                        time.sleep(sleep_time)
                        wait_seconds -= sleep_time
                        
                        if not self.is_within_active_hours():
                            break
                
                if self.is_running and self.is_within_active_hours():
                    if self.should_run_scheduled_task(task_config):
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Executing scheduled task: {task_config['task']}")
                        self.execute_task_by_name(task_config['task'])
            
            time.sleep(30)
    
    def random_behavior_cycle(self):
        print("Running in random mode")
        while self.is_running:
            for session in range(self.config['daily_sessions']):
                if not self.is_running:
                    break
                
                self.wait_for_active_hours()
                
                if not self.is_running:
                    break
                
                session_duration = random.randint(*self.config['session_duration_minutes'])
                session_end_time = datetime.now() + timedelta(minutes=session_duration)
                
                activities = [
                    self.browse_websites,
                    self.watch_youtube,
                    self.create_text_files,
                    self.download_media,
                    self.share_files_with_network,
                    self.ping_target_ips
                ]
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting session {session + 1}/{self.config['daily_sessions']} for {session_duration} minutes")
                
                while datetime.now() < session_end_time and self.is_running and self.is_within_active_hours():
                    activity = random.choice(activities)
                    try:
                        activity()
                    except:
                        pass
                
                if self.is_running and session < self.config['daily_sessions'] - 1:
                    session_break = random.randint(1800, 7200)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Session break for {int(session_break/60)} minutes")
                    time.sleep(session_break)
            
            if self.is_running:
                next_day_sleep = random.randint(18000, 28800)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Daily cycle complete, sleeping for {int(next_day_sleep/3600)} hours")
                time.sleep(next_day_sleep)
    
    def start(self):
        self.is_running = True
        
        receiver_thread = self.start_file_receiver()
        self.threads.append(receiver_thread)
        receiver_thread.start()
        
        if self.config['scheduled_tasks']['enabled']:
            behavior_thread = threading.Thread(target=self.scheduled_behavior_cycle)
        else:
            behavior_thread = threading.Thread(target=self.random_behavior_cycle)
            
        behavior_thread.daemon = True
        self.threads.append(behavior_thread)
        behavior_thread.start()
        
        print(f"User behavior simulation started at {datetime.now().strftime('%H:%M:%S')}. Press Ctrl+C to stop.")
        
        if self.config['active_hours']['enabled']:
            print(f"Active hours: {self.config['active_hours']['start_hour']:02d}:00 - {self.config['active_hours']['end_hour']:02d}:00")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.is_running = False
        print("Stopping user behavior simulation...")
        
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1)