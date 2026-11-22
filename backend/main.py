
from flask import Flask, jsonify
from datetime import datetime, timezone
import socket
import requests
import feedparser
import re
import ipaddress

app = Flask(__name__)

APP_NAME = "074CyberToolsV1.0"
DEVELOPER = "ereecx1st"
VERSION = "1.1.0"

@app.route("/")
def home():
    return jsonify({
        "application": APP_NAME,
        "developer": DEVELOPER,
        "status": "online",
        "version": VERSION,
        "modules": [
            "Health Check",
            "IP Intelligence",
            "DNS Lookup",
            "World News"
        ]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": APP_NAME,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    })

@app.route("/ip")
def get_ip():
    providers = [
        ("ipify", "https://api.ipify.org?format=json", True),
        ("ifconfig.me", "https://ifconfig.me/ip", False),
        ("icanhazip", "https://icanhazip.com", False)
    ]

    errors = []

    for name, url, is_json in providers:
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "074CyberToolsV1.0/1.1"}
            )
            response.raise_for_status()

            value = (
                response.json().get("ip")
                if is_json
                else response.text.strip()
            )

            address = str(ipaddress.ip_address(value))

            return jsonify({
                "status": "success",
                "application": APP_NAME,
                "provider": name,
                "ip": address,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat()
            })

        except Exception as error:
            errors.append({
                "provider": name,
                "reason": str(error)[:150]
            })

    return jsonify({
        "status": "error",
        "message": "All IP providers unavailable",
        "providers": errors
    }), 503

@app.route("/dns/<domain>")
def dns_lookup(domain):
    if not re.fullmatch(
        r"[A-Za-z0-9.-]{1,253}", domain
    ):
        return jsonify({
            "error": "Invalid domain"
        }), 400

    try:
        results = socket.getaddrinfo(
            domain, None, socket.AF_INET
        )

        addresses = sorted({
            item[4][0] for item in results
        })

        return jsonify({
            "status": "success",
            "domain": domain,
            "ipv4": addresses
        })

    except socket.gaierror:
        return jsonify({
            "error": "DNS record unavailable"
        }), 404

@app.route("/news")
def world_news():
    try:
        feed = feedparser.parse(
            "https://feeds.bbci.co.uk/news/world/rss.xml"
        )

        articles = [{
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "published": item.get("published", "")
        } for item in feed.entries[:10]]

        if not articles:
            return jsonify({
                "error": "News unavailable"
            }), 503

        return jsonify({
            "status": "success",
            "source": "BBC News",
            "updated": datetime.now(
                timezone.utc
            ).isoformat(),
            "articles": articles
        })

    except Exception:
        return jsonify({
            "error": "News service unavailable"
        }), 503

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
	
