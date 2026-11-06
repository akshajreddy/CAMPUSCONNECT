#!/usr/bin/env python3
"""
CampusConnect - Automated Vercel API Deployment Script
Deploys the static React landing page directly to Vercel via Vercel REST API.
Usage:
    python deploy_vercel.py [VERCEL_TOKEN]
"""

import os
import sys
import json
import hashlib
import urllib.request
import urllib.error

PROJECT_NAME = "campusconnect-app"

def upload_file_to_vercel(file_bytes, token):
    """Uploads a file to Vercel and returns its SHA hash."""
    sha = hashlib.sha1(file_bytes).hexdigest()
    url = "https://api.vercel.com/v2/files"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Length": str(len(file_bytes)),
        "x-vercel-digest": sha,
        "Content-Type": "application/octet-stream"
    }
    
    req = urllib.request.Request(url, data=file_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            pass
    except urllib.error.HTTPError as e:
        # Status 200 or already uploaded can happen, which is fine
        if e.code not in (200, 409):
            error_msg = e.read().decode('utf-8', errors='ignore')
            print(f"Warning on file upload ({sha[:8]}): {e.code} {error_msg}")
    return sha

def deploy_to_vercel(token):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files_to_deploy = ["index.html", "vercel.json", "package.json"]
    
    file_manifest = []
    print(" [*] Preparing and uploading files to Vercel Edge Network...")
    
    for fname in files_to_deploy:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "rb") as f:
            data = f.read()
            sha = upload_file_to_vercel(data, token)
            file_manifest.append({
                "file": fname,
                "sha": sha,
                "size": len(data)
            })
            print(f"  + Uploaded {fname} ({len(data)} bytes, sha: {sha[:10]}...)")
            
    payload = {
        "name": PROJECT_NAME,
        "files": file_manifest,
        "projectSettings": {
            "framework": None,
            "buildCommand": None,
            "outputDirectory": "."
        },
        "target": "production"
    }
    
    deploy_url = "https://api.vercel.com/v13/deployments"
    req_data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(deploy_url, data=req_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            live_url = res_data.get("url")
            alias_list = res_data.get("alias", [])
            
            print("\n" + "=" * 60)
            print("  SUCCESS! CampusConnect is DEPLOYED LIVE ON VERCEL!")
            print("=" * 60)
            print(f"\n  Live Deployment URL: https://{live_url}")
            for a in alias_list:
                print(f"  Primary Production URL: https://{a}")
            print("\n  This link is permanent, public, and requires no login.")
            print("  You can submit this URL directly for your Wadhwani NEN assignment.")
            print("=" * 60 + "\n")
            return f"https://{live_url}"
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        print(f"\n[!] Vercel deployment error ({e.code}): {err}")
        return None

if __name__ == "__main__":
    token = os.environ.get("VERCEL_TOKEN")
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
        
    if not token:
        print("\n" + "=" * 60)
        print(" CampusConnect Vercel Deployment Helper")
        print("=" * 60)
        print("\nPlease provide your Vercel Access Token:")
        print(" 1. Go to https://vercel.com/account/tokens")
        print(" 2. Click 'Create Token', give it a name (e.g. 'campusconnect'), and copy it.")
        print(" 3. Run: python deploy_vercel.py <YOUR_TOKEN>\n")
        try:
            token = input("Or paste your Vercel Token here and press Enter: ").strip()
        except EOFError:
            pass
            
    if token:
        deploy_to_vercel(token)
    else:
        print("[!] No token provided. Exiting.")
