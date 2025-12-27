import instaloader
import requests
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
COMPETITORS = ['mabuzar.111'] # Competitor Instagram Handles
N8N_WEBHOOK_URL = "https://abuzar5533.app.n8n.cloud/webhook/instagram-spy" \
"" 

# NUMBER OF  POSTS TO CHECK PER COMPETITOR
POSTS_TO_CHECK = 5

# VIRAL THRESHOLD
VIRAL_THRESHOLD_PERCENT = 2.0

# --- END CONFIGURATION ---
HISTORY_FILE = "sent_posts_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_history(history_set):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(list(history_set), f)

def get_recent_posts():
    L = instaloader.Instaloader()
    # L.login("USER", "PASSWORD")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🕵️  Checking Last {POSTS_TO_CHECK} Posts...")
    
    sent_posts = load_history()
    new_sent_posts = sent_posts.copy()
    
    for username in COMPETITORS:
        print(f"    Analyzing: {username}...")
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            followers = profile.followers
            
            #  initialize Counter
            count = 0
            
            for post in profile.get_posts():
                # --- LOGIC TO STOP AFTER 5 POSTS ---
                if count >= POSTS_TO_CHECK:
                    print(f"    Checked latest {POSTS_TO_CHECK} posts. Moving to next user.")
                    break
                
                count += 1 
                
               
                if post.shortcode in sent_posts:
                    print(f"      • Post {post.shortcode} already sent. Skipping.")
                    continue

                
                likes = post.likes
                comments = post.comments
                engagement_rate = ((likes + comments) / followers) * 100 if followers > 0 else 0
                is_viral = engagement_rate > VIRAL_THRESHOLD_PERCENT
                
                payload = {
                    "competitor": username,
                    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "image_url": post.url,
                    "caption": post.caption[:200] + "..." if post.caption else "",
                    "likes": likes,
                    "comments": comments,
                    "engagement_rate": round(engagement_rate, 2),
                    "is_viral": is_viral,
                    "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }

                print(f"       Sending NEW post to n8n...")
                
                if send_to_n8n(payload):
                    new_sent_posts.add(post.shortcode)
                
        except Exception as e:
            print(f"    Error checking {username}: {e}")

    save_history(new_sent_posts)
    print("All Done.")

def send_to_n8n(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(N8N_WEBHOOK_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"       n8n Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"       Connection Error: {e}")
        return False

if __name__ == "__main__":
    get_recent_posts()
