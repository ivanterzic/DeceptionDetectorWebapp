import threading
import time
import schedule
from model_trainer import cleanup_expired_models


class CleanupService:
    """Background service to clean up expired models."""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the cleanup service."""
        if self.running:
            return
        
        print("🧹 Starting model cleanup service")
        self.running = True
        
        # Schedule cleanup every 6 hours
        schedule.every(6).hours.do(self._run_cleanup)
        
        # Also schedule a daily cleanup at 2 AM
        schedule.every().day.at("02:00").do(self._run_cleanup)
        
        # Start the scheduler thread
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        
        # Run initial cleanup
        self._run_cleanup()
    
    def stop(self):
        """Stop the cleanup service."""
        if not self.running:
            return
        
        print("🛑 Stopping model cleanup service")
        self.running = False
        schedule.clear()
    
    def _run_cleanup(self):
        """Run the cleanup process."""
        try:
            print("🧹 Running scheduled model cleanup")
            cleanup_expired_models()
        except Exception as e:
            print(f"❌ Cleanup service error: {str(e)}")
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


# Global cleanup service instance
cleanup_service = CleanupService()