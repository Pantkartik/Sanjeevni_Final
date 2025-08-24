#!/usr/bin/env python3
"""
Simplified Development Server Startup Script
Starts Django development server without Redis/Celery dependencies
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class SimpleDevServer:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def check_manage_py(self):
        """Check if manage.py exists"""
        if not Path('manage.py').exists():
            print("❌ manage.py not found. Please run this script from the backend directory.")
            return False
        return True
    
    def start_django(self):
        """Start Django development server"""
        try:
            print("🚀 Starting Django development server...")
            process = subprocess.Popen(
                [sys.executable, 'manage.py', 'runserver'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(('Django Server', process))
            print("✅ Django server started successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to start Django server: {e}")
            return False
    
    def start_all_services(self):
        """Start all development services"""
        print("🚀 Starting Sanjeevni Development Environment (Simplified)")
        print("=" * 50)
        
        if not self.check_manage_py():
            return False
        
        if not self.start_django():
            return False
        
        print("\n🎉 Django server started successfully!")
        print("\n📱 Access your application:")
        print("   • Frontend: http://localhost:3000")
        print("   • Backend API: http://localhost:8000")
        print("   • Django Admin: http://localhost:8000/admin")
        print("\n🔑 Default superuser: admin/admin")
        print("\n💡 To start the frontend, open a new terminal and run:")
        print("   cd ../frontend && npm run dev")
        print("\n⏹️  Press Ctrl+C to stop all services")
        
        return True
    
    def monitor_processes(self):
        """Monitor running processes"""
        while self.running:
            for name, process in self.processes:
                if process.poll() is not None:
                    print(f"⚠️  {name} has stopped unexpectedly")
                    self.running = False
                    break
            time.sleep(1)
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️  {name} force killed")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        print("✅ All services stopped")
    
    def run(self):
        """Main run method"""
        try:
            if not self.start_all_services():
                return
            
            # Start monitoring in background
            monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            monitor_thread.start()
            
            # Wait for user interrupt
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Received interrupt signal...")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.stop_all_services()

def main():
    """Main entry point"""
    server = SimpleDevServer()
    server.run()

if __name__ == "__main__":
    main()
