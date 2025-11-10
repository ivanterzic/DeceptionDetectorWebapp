"""
Generate secure secrets for production deployment

This script generates:
- JWT_SECRET: Used to sign JWT tokens
- Password hash for API authentication

⚠️  IMPORTANT: Store these values securely and never commit them to Git!
"""

import secrets
import hashlib
import getpass
import os

def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_secrets():
    print("="*70)
    print("🔐 SECURE SECRETS FOR PRODUCTION")
    print("="*70)
    print()
    print("⚠️  WARNING: These are sensitive credentials!")
    print("   • Never commit to Git")
    print("   • Store in secure vault or environment variables")
    print("   • Rotate regularly (every 90 days recommended)")
    print()
    print("="*70)
    print()
    
    # Get custom password or use generated one
    print("Choose option:")
    print("1. Enter your own password")
    print("2. Generate random password")
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        password = getpass.getpass("Enter API password: ")
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("❌ Passwords don't match!")
            return
    else:
        password = secrets.token_urlsafe(16)
        print(f"Generated password: {password}")
        print("⚠️  Save this password - you'll need it for API access!")
        print()
    
    password_hash = hash_password(password)
    jwt_secret = secrets.token_urlsafe(32)
    
    print()
    print("📋 COPY THESE VALUES TO YOUR ENVIRONMENT:")
    print()
    print(f"API_USERNAME=externalapiuser")
    print(f"API_PASSWORD={password}")
    print(f"JWT_SECRET={jwt_secret}")
    print(f"JWT_EXP_SECONDS=3600")
    print()
    print("ℹ️  Note: Password is stored in plain text (server-side only)")
    print("   Clients must hash with SHA256 before sending:")
    print(f"   Password Hash (for reference): {password_hash}")
    print()
    print("="*70)
    print()
    print("💻 HOW TO USE:")
    print()
    
    print("Windows (PowerShell):")
    print(f'  $env:API_USERNAME="externalapiuser"')
    print(f'  $env:API_PASSWORD="{password}"')
    print(f'  $env:JWT_SECRET="{jwt_secret}"')
    print('  $env:JWT_EXP_SECONDS="3600"')
    print()
    
    print("Linux/Mac (bash):")
    print(f'  export API_USERNAME="externalapiuser"')
    print(f'  export API_PASSWORD="{password}"')
    print(f'  export JWT_SECRET="{jwt_secret}"')
    print('  export JWT_EXP_SECONDS="3600"')
    print()
    
    print("="*70)
    print()
    
    # Ask if user wants to update .env file
    update_env = input("\n💾 Update backend/.env file automatically? (y/n): ").strip().lower()
    
    if update_env == 'y':
        env_path = 'backend/.env'
        try:
            # Read existing .env or create from example
            if not os.path.exists(env_path):
                if os.path.exists('backend/.env.example'):
                    import shutil
                    shutil.copy('backend/.env.example', env_path)
            
            # Update .env file
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('API_USERNAME='):
                        f.write(f'API_USERNAME=externalapiuser\n')
                    elif line.startswith('API_PASSWORD_HASH='):
                        # Replace old hash line with new password line
                        f.write(f'API_PASSWORD={password}\n')
                    elif line.startswith('API_PASSWORD='):
                        f.write(f'API_PASSWORD={password}\n')
                    elif line.startswith('JWT_SECRET='):
                        f.write(f'JWT_SECRET={jwt_secret}\n')
                    else:
                        f.write(line)
            
            print(f"✅ Updated {env_path} successfully!")
            print("   Restart the backend to apply changes.")
        except Exception as e:
            print(f"❌ Failed to update .env file: {e}")
            print("   You can manually copy the values above.")
    
    print()
    print("✅ Secrets generated successfully!")
    print(f"📝 API Password: {password}")
    print("📖 See API_USAGE.md for usage instructions")
    print()

if __name__ == "__main__":
    generate_secrets()
