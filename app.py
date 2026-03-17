# index.py - Sahi wala with Old Email field
from flask import Flask, request, jsonify, render_template_string
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

HEADERS = {
    "User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# SAHI HTML - With Old Email Field
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>BAKI FF TOOL | Master Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); border-radius: 1.5rem; padding: 1.5rem; margin-bottom: 1rem; }
        input { background: #0f172a; border: 1px solid #1e293b; padding: 0.8rem; border-radius: 0.8rem; width: 100%; margin-bottom: 0.6rem; color: white; outline: none; font-size: 14px; }
        input:focus { border-color: #3b82f6; }
        .btn { width: 100%; padding: 0.9rem; border-radius: 1rem; font-weight: 800; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; transition: 0.2s; }
        .console { background: #000; border-radius: 1rem; padding: 0.75rem; font-family: monospace; font-size: 11px; color: #4ade80; max-height: 150px; overflow: auto; margin-top: 1rem; border: 1px solid #1e293b; }
        .status-badge { font-size: 10px; padding: 2px 8px; border-radius: 99px; background: rgba(59, 130, 246, 0.1); color: #3b82f6; font-weight: bold; margin-bottom: 8px; display: inline-block; }
        .step-badge { font-size: 10px; color: #fbbf24; margin-bottom: 10px; display: block; }
    </style>
</head>
<body class="p-4 max-w-xl mx-auto pb-10">

    <header class="text-center py-8">
        <h1 class="text-4xl font-black text-blue-500 italic tracking-tighter">BAKI</h1>
        <p class="text-slate-500 text-[10px] uppercase tracking-[0.3em] mt-1">Garena Tool Suite</p>
    </header>

    <!-- EAT DECODER -->
    <div class="glass border-green-500/20">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-green-400 font-bold uppercase text-[10px] tracking-widest"><i class="fas fa-key mr-2"></i> Eat Token Decoder</h3>
            <span class="text-[10px] text-slate-500">Auto Fill</span>
        </div>
        <input type="text" id="eat_input" placeholder="Paste EAT Token Here">
        <button onclick="decodeEat()" class="btn bg-green-600 hover:bg-green-500 shadow-lg shadow-green-900/20">Decode & Auto-Fill</button>
        <pre id="decode_out" class="console hidden"></pre>
    </div>

    <!-- BIND EMAIL -->
    <div class="glass border-purple-500/20">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-purple-400 font-bold uppercase text-[10px] tracking-widest"><i class="fas fa-plus mr-2"></i> Bind New Email</h3>
            <span class="text-[10px] text-slate-500">New Account</span>
        </div>
        <input type="text" id="bind_token" placeholder="Access Token">
        <input type="email" id="bind_email" placeholder="New Email to Bind">
        <button onclick="bindEmail()" class="btn bg-purple-600">Send OTP & Bind</button>
        <div id="bind_otp_div" class="hidden mt-2">
            <input type="text" id="bind_otp" placeholder="Enter OTP">
            <button onclick="confirmBind()" class="btn bg-purple-500">Confirm Bind</button>
        </div>
        <pre id="bind_out" class="console hidden"></pre>
    </div>

    <!-- CHANGE EMAIL -->
    <div class="glass border-blue-500/20">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-blue-400 font-bold uppercase text-[10px] tracking-widest"><i class="fas fa-sync-alt mr-2"></i> Change Email</h3>
            <span class="text-[10px] text-slate-500">Replace Old</span>
        </div>
        
        <span class="step-badge">Step 1: Enter Details</span>
        <input type="text" id="change_token" placeholder="Access Token">
        <input type="email" id="old_email" placeholder="OLD EMAIL (OTP will be sent here)">
        <input type="email" id="new_email" placeholder="NEW EMAIL (To be bound)">
        
        <div class="flex gap-2 mb-4">
            <button onclick="setChangeMode('otp')" class="flex-1 bg-slate-800 py-2 rounded-lg text-[10px] font-bold border border-slate-700 text-orange-400">USE OTP</button>
            <button onclick="setChangeMode('sec')" class="flex-1 bg-slate-800 py-2 rounded-lg text-[10px] font-bold border border-slate-700">USE SECURITY CODE</button>
        </div>

        <!-- OTP Mode -->
        <div id="change_otp_mode">
            <button onclick="sendChangeOldOtp()" class="btn bg-orange-600 mb-2">1. Send OTP to OLD Email</button>
            <input type="text" id="change_old_otp" placeholder="OTP from OLD Email">
            <button onclick="verifyChangeIdent('otp')" class="btn bg-blue-600">2. Verify OLD Email</button>
        </div>

        <!-- Security Code Mode -->
        <div id="change_sec_mode" class="hidden">
            <input type="text" id="change_sec_code" placeholder="Enter Security Code">
            <button onclick="verifyChangeIdent('sec')" class="btn bg-blue-600">Verify & Continue</button>
        </div>

        <!-- Step 2: New Email -->
        <div id="change_step2" class="hidden mt-6 pt-6 border-t border-slate-700/50">
            <span class="step-badge">Step 2: Verify New Email</span>
            <div class="status-badge">Old Email Verified ✓</div>
            <button onclick="sendChangeNewOtp()" class="btn bg-green-600 mb-2">3. Send OTP to NEW Email</button>
            <div id="change_final_div" class="hidden mt-2">
                <input type="text" id="change_new_otp" placeholder="OTP from NEW Email">
                <button onclick="finalizeChange()" class="btn bg-blue-500">4. Finalize Change</button>
            </div>
        </div>
        <pre id="change_out" class="console hidden"></pre>
    </div>

    <!-- UNBIND EMAIL -->
    <div class="glass border-red-500/20">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-red-400 font-bold uppercase text-[10px] tracking-widest"><i class="fas fa-unlink mr-2"></i> Unbind Email</h3>
            <span class="text-[10px] text-slate-500">Remove Recovery</span>
        </div>
        <input type="text" id="unbind_token" placeholder="Access Token">
        <input type="email" id="unbind_email" placeholder="Current Email (OTP will be sent here)">
        
        <div class="flex gap-2 mb-4">
            <button onclick="setUnbindMode('otp')" class="flex-1 bg-slate-800 py-2 rounded-lg text-[10px] font-bold border border-slate-700 text-orange-400">USE OTP</button>
            <button onclick="setUnbindMode('sec')" class="flex-1 bg-slate-800 py-2 rounded-lg text-[10px] font-bold border border-slate-700">USE SECURITY CODE</button>
        </div>

        <div id="unbind_otp_mode">
            <button onclick="sendUnbindOtp()" class="btn bg-orange-600 mb-2">Send OTP to Email</button>
            <input type="text" id="unbind_otp" placeholder="Enter OTP">
            <button onclick="doUnbind('otp')" class="btn btn-danger bg-red-600">Unbind Now</button>
        </div>

        <div id="unbind_sec_mode" class="hidden">
            <input type="text" id="unbind_sec" placeholder="Enter Security Code">
            <button onclick="doUnbind('sec')" class="btn btn-danger bg-red-600">Unbind Now</button>
        </div>
        <pre id="unbind_out" class="console hidden"></pre>
    </div>

    <!-- ACCOUNT UTILITIES -->
    <div class="glass">
        <h3 class="text-slate-400 font-bold mb-4 uppercase text-[10px] tracking-widest"><i class="fas fa-tools mr-2"></i> Account Utilities</h3>
        <input type="text" id="util_token" placeholder="Access Token">
        <div class="grid grid-cols-1 gap-2">
            <button onclick="util('check')" class="btn bg-slate-800">Check Bind Status (With Real Time)</button>
            <button onclick="util('cancel')" class="btn bg-orange-900/40 border border-orange-700/30">Cancel Pending Request</button>
            <button onclick="util('links')" class="btn bg-purple-900/40 border border-purple-700/30">View Linked Platforms</button>
            <button onclick="util('revoke')" class="btn bg-red-600/20 border border-red-900/40 text-red-500">Revoke Access Token</button>
        </div>
        <pre id="util_out" class="console hidden"></pre>
    </div>

    <script>
        // Global session
        let session = {
            bind: { token: '', email: '' },
            change: { token: '', old_email: '', new_email: '', identity: '' },
            unbind: { token: '', email: '' }
        };

        // ========== EAT DECODER ==========
        async function decodeEat() {
            const eat = document.getElementById('eat_input').value;
            const out = document.getElementById('decode_out');
            out.classList.remove('hidden');
            
            const res = await fetch('/api/decode', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({eat_token: eat})
            });
            const data = await res.json();
            
            if(data.access_token) {
                // Auto fill all fields
                document.getElementById('bind_token').value = data.access_token;
                document.getElementById('change_token').value = data.access_token;
                document.getElementById('unbind_token').value = data.access_token;
                document.getElementById('util_token').value = data.access_token;
                out.innerText = `✓ Decoded! Token auto-filled everywhere.`;
            } else {
                out.innerText = '✗ Invalid EAT Token';
            }
        }

        // ========== BIND EMAIL ==========
        async function bindEmail() {
            session.bind.token = document.getElementById('bind_token').value;
            session.bind.email = document.getElementById('bind_email').value;
            
            await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: 'send_otp',
                    token: session.bind.token,
                    email: session.bind.email
                })
            });
            
            document.getElementById('bind_otp_div').classList.remove('hidden');
            alert('OTP sent to ' + session.bind.email);
        }

        async function confirmBind() {
            const otp = document.getElementById('bind_otp').value;
            const out = document.getElementById('bind_out');
            out.classList.remove('hidden');
            
            // Verify OTP
            const vRes = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: 'verify_otp',
                    token: session.bind.token,
                    email: session.bind.email,
                    otp: otp
                })
            });
            const vData = await vRes.json();
            
            if(vData.verifier_token) {
                // Cancel any pending
                await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'cancel',
                        token: session.bind.token
                    })
                });
                
                // Create bind
                const bRes = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'create_bind',
                        token: session.bind.token,
                        email: session.bind.email,
                        verifier: vData.verifier_token
                    })
                });
                const bData = await bRes.json();
                out.innerText = bData.result === 0 ? 
                    `✓ BIND CREATED!\\nEmail: ${session.bind.email}\\nConfirm in: 3 days (259200 seconds)` : 
                    `✗ Failed: ${JSON.stringify(bData)}`;
            } else {
                out.innerText = '✗ Invalid OTP';
            }
        }

        // ========== CHANGE EMAIL ==========
        function setChangeMode(mode) {
            document.getElementById('change_otp_mode').classList.toggle('hidden', mode !== 'otp');
            document.getElementById('change_sec_mode').classList.toggle('hidden', mode !== 'sec');
        }

        async function sendChangeOldOtp() {
            session.change.token = document.getElementById('change_token').value;
            session.change.old_email = document.getElementById('old_email').value;
            session.change.new_email = document.getElementById('new_email').value;
            
            await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: 'send_otp',
                    token: session.change.token,
                    email: session.change.old_email
                })
            });
            alert('OTP sent to OLD email: ' + session.change.old_email);
        }

        async function verifyChangeIdent(type) {
            let payload = {
                action: 'verify_identity',
                token: session.change.token,
                email: session.change.old_email
            };
            
            if(type === 'otp') {
                payload.otp = document.getElementById('change_old_otp').value;
            } else {
                payload.code = document.getElementById('change_sec_code').value;
            }
            
            const res = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            if(data.identity_token) {
                session.change.identity = data.identity_token;
                document.getElementById('change_step2').classList.remove('hidden');
                alert('✓ Old Email Verified! Now verify new email.');
            } else {
                alert('✗ Verification Failed');
            }
        }

        async function sendChangeNewOtp() {
            await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: 'send_otp',
                    token: session.change.token,
                    email: session.change.new_email
                })
            });
            document.getElementById('change_final_div').classList.remove('hidden');
            alert('OTP sent to NEW email: ' + session.change.new_email);
        }

        async function finalizeChange() {
            const otp = document.getElementById('change_new_otp').value;
            const out = document.getElementById('change_out');
            out.classList.remove('hidden');
            
            // Verify new OTP
            const vRes = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: 'verify_otp',
                    token: session.change.token,
                    email: session.change.new_email,
                    otp: otp
                })
            });
            const vData = await vRes.json();
            
            if(vData.verifier_token) {
                // Create rebind
                const rRes = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'create_rebind',
                        token: session.change.token,
                        identity: session.change.identity,
                        verifier: vData.verifier_token,
                        email: session.change.new_email
                    })
                });
                const rData = await rRes.json();
                
                // Calculate real date
                const target = new Date();
                target.setSeconds(target.getSeconds() + 259200);
                
                out.innerText = rData.result === 0 ? 
                    `✓ CHANGE REQUEST CREATED!\\nOld: ${session.change.old_email}\\nNew: ${session.change.new_email}\\nConfirm Date: ${target.toLocaleString()}\\n(3 days from now)` : 
                    `✗ Failed: ${JSON.stringify(rData)}`;
            } else {
                out.innerText = '✗ Invalid New Email OTP';
            }
        }

        // ========== UNBIND EMAIL ==========
        function setUnbindMode(mode) {
            document.getElementById('unbind_otp_mode').classList.toggle('hidden', mode !== 'otp');
            document.getElementById('unbind_sec_mode').classList.toggle('hidden', mode !== 'sec');
        }

        async function sendUnbindOtp() {
            session.unbind.token = document.getElementById('unbind_token').value;
            session.unbind.email = document.getElementById('unbind_email').value;
            
            await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: 'send_otp',
                    token: session.unbind.token,
                    email: session.unbind.email
                })
            });
            alert('OTP sent to: ' + session.unbind.email);
        }

        async function doUnbind(type) {
            const out = document.getElementById('unbind_out');
            out.classList.remove('hidden');
            
            let payload = {
                action: 'verify_identity',
                token: session.unbind.token || document.getElementById('unbind_token').value,
                email: session.unbind.email || document.getElementById('unbind_email').value
            };
            
            if(type === 'otp') {
                payload.otp = document.getElementById('unbind_otp').value;
            } else {
                payload.code = document.getElementById('unbind_sec').value;
            }
            
            // Verify
            const vRes = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const vData = await vRes.json();
            
            if(vData.identity_token) {
                // Create unbind
                const uRes = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'create_unbind',
                        token: payload.token,
                        identity: vData.identity_token
                    })
                });
                const uData = await uRes.json();
                
                const target = new Date();
                target.setSeconds(target.getSeconds() + 259200);
                
                out.innerText = uData.result === 0 ? 
                    `✓ UNBIND REQUEST CREATED!\\nEmail will be removed on: ${target.toLocaleString()}\\n(3 days from now)` : 
                    `✗ Failed: ${JSON.stringify(uData)}`;
            } else {
                out.innerText = '✗ Verification Failed';
            }
        }

        // ========== UTILITIES ==========
        async function util(action) {
            const token = document.getElementById('util_token').value;
            const out = document.getElementById('util_out');
            out.classList.remove('hidden');
            
            const res = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action, token})
            });
            const data = await res.json();
            
            if(action === 'check' && data.request_exec_countdown) {
                const target = new Date();
                target.setSeconds(target.getSeconds() + data.request_exec_countdown);
                const days = Math.floor(data.request_exec_countdown / 86400);
                const hours = Math.floor((data.request_exec_countdown % 86400) / 3600);
                const mins = Math.floor((data.request_exec_countdown % 3600) / 60);
                const secs = data.request_exec_countdown % 60;
                
                out.innerText = `Status: ${data.email_to_be ? 'PENDING' : (data.email ? 'CONFIRMED' : 'NONE')}\\n` +
                    (data.email ? `Current: ${data.email}\\n` : '') +
                    (data.email_to_be ? `Pending: ${data.email_to_be}\\n` : '') +
                    `\\n⏰ REAL TIME COUNTDOWN:\\n` +
                    `Confirm Date: ${target.toLocaleString()}\\n` +
                    `Time Left: ${days}d ${hours}h ${mins}m ${secs}s\\n` +
                    `Raw Seconds: ${data.request_exec_countdown}`;
            } else {
                out.innerText = JSON.stringify(data, null, 2);
            }
        }
    </script>
</body>
</html>'''

def convert_time(total_seconds):
    if total_seconds <= 0:
        return "EXPIRED", "0d 0h 0m 0s"
    target_date = datetime.now() + timedelta(seconds=total_seconds)
    date_str = target_date.strftime("%Y-%m-%d %H:%M:%S")
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    time_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
    return date_str, time_str

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/decode', methods=['POST'])
def decode():
    try:
        data = request.get_json()
        eat = data.get('eat_token', '')
        params = {}
        for pair in eat.split('&'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k] = v
        return jsonify({
            "access_token": params.get('access_token', ''),
            "account_id": params.get('account_id', ''),
            "open_id": params.get('openid', '')
        })
    except:
        return jsonify({"error": "Invalid EAT"})

@app.route('/api/action', methods=['POST'])
def action():
    try:
        data = request.get_json()
        act = data.get('action')
        token = data.get('token')
        
        # 1. SEND OTP
        if act == 'send_otp':
            url = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
            payload = {
                'app_id': "100067",
                'access_token': token,
                'email': data.get('email'),
                'locale': "en_MA",
                'region': 'IND'
            }
            r = requests.post(url, data=payload, headers=HEADERS, timeout=10)
            return jsonify(r.json())
        
        # 2. VERIFY OTP (for new email)
        elif act == 'verify_otp':
            url = "https://100067.connect.garena.com/game/account_security/bind:verify_otp"
            payload = {
                'app_id': "100067",
                'access_token': token,
                'email': data.get('email'),
                'otp': data.get('otp')
            }
            r = requests.post(url, data=payload, headers=HEADERS, timeout=10)
            return jsonify(r.json())
        
        # 3. VERIFY IDENTITY (for old email - OTP or Security Code)
        elif act == 'verify_identity':
            url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
            payload = {
                'app_id': "100067",
                'access_token': token,
                'email': data.get('email')
            }
            if 'otp' in data:
                payload['otp'] = data['otp']
            else:
                payload['secondary_password'] = data.get('code')
            r = requests.post(url, data=payload, headers=HEADERS, timeout=10)
            return jsonify(r.json())
        
        # 4. CREATE BIND
        elif act == 'create_bind':
            url = "https://100067.connect.garena.com/game/account_security/bind:create_bind_request"
            payload = {
                'app_id': "100067",
                'access_token': token,
                'verifier_token': data.get('verifier'),
                'secondary_password': "91B4D142823F7D20C5F08DF69122DE43F35F057A988D9619F6D3138485C9A203",
                'email': data.get('email')
            }
            r = requests.post(url, data=payload, headers=HEADERS, timeout=10)
            result = r.json()
            if result.get('result') == 0:
                date_str, time_str = convert_time(259200)
                result['confirmation_date'] = date_str
                result['time_remaining'] = time_str
            return jsonify(result)
        
        # 5. CREATE REBIND (Change Email)
        elif act == 'create_rebind':
            url = "https://100067.connect.garena.com/game/account_security/bind:create_rebind_request"
            payload = {
                'app_id': "100067",
                'access_token': token,
                'identity_token': data.get('identity'),
                'verifier_token': data.get('verifier'),
                'email': data.get('email')
            }
            r = requests.post(url, data=payload, headers=HEADERS, timeout=10)
            result = r.json()
            if result.get('result') == 0:
                date_str, time_str = convert_time(259200)
                result['confirmation_date'] = date_str
                result['time_remaining'] = time_str
            return jsonify(result)
        
        # 6. CREATE UNBIND
        elif act == 'create_unbind':
            url = "https://100067.connect.garena.com/game/account_security/bind:create_unbind_request"
            payload = {
                'app_id': "100067",
                'access_token': token,
                'identity_token': data.get('identity')
            }
            r = requests.post(url, data=payload, headers=HEADERS, timeout=10)
            result = r.json()
            if result.get('result') == 0:
                date_str, time_str = convert_time(259200)
                result['confirmation_date'] = date_str
                result['time_remaining'] = time_str
            return jsonify(result)
        
        # 7. CANCEL
        elif act == 'cancel':
            url = "https://100067.connect.garena.com/game/account_security/bind:cancel_request"
            payload = {'app_id': "100067", 'access_token': token}
            headers = {
                'User-Agent': HEADERS['User-Agent'],
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip"
            }
            r = requests.post(url, data=payload, headers=headers, timeout=10)
            return jsonify(r.json())
        
        # 8. CHECK STATUS
        elif act == 'check':
            url = "https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
            payload = {'app_id': "100067", 'access_token': token}
            headers = {
                'User-Agent': HEADERS['User-Agent'],
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip"
            }
            r = requests.get(url, params=payload, headers=headers, timeout=10)
            result = r.json()
            
            countdown = result.get('request_exec_countdown', 0)
            if countdown > 0:
                date_str, time_str = convert_time(countdown)
                result['confirmation_date'] = date_str
                result['time_remaining'] = time_str
            
            return jsonify(result)
        
        # 9. LINKS
        elif act == 'links':
            url = "https://100067.connect.garena.com/bind/app/platform/info/get"
            headers = {
                'User-Agent': HEADERS['User-Agent'],
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "If-Modified-Since": "Sun, 18 May 2025 09:37:03 GMT"
            }
            r = requests.get(url, params={'access_token': token}, headers=headers, timeout=10)
            if r.status_code in [200, 201]:
                j = r.json()
                platforms = {3: "Facebook", 8: "Gmail", 10: "iCloud", 5: "VK", 11: "Twitter", 7: "Huawei"}
                result = {"linked": [], "main": None}
                
                for x in j.get("bounded_accounts", []):
                    p = x.get('platform')
                    if p in platforms:
                        result["linked"].append({
                            "platform": platforms[p],
                            "uid": x.get('uid'),
                            "email": x.get('user_info', {}).get('email', ''),
                            "name": x.get('user_info', {}).get('nickname', '')
                        })
                
                for k in platforms:
                    if k not in j.get("available_platforms", []):
                        result["main"] = platforms[k]
                        break
                
                return jsonify(result)
            return jsonify({"error": "Failed", "status": r.status_code})
        
        # 10. REVOKE
        elif act == 'revoke':
            url = f"https://100067.connect.garena.com/oauth/logout?access_token={token}"
            r = requests.get(url, timeout=10)
            if r.text.strip() == '{"result":0}':
                return jsonify({"result": 0, "message": "TOKEN REVOKED"})
            return jsonify({"result": -1, "response": r.text})
        
        else:
            return jsonify({"error": "Unknown action"})
            
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🔥 STILLRARE Running on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
