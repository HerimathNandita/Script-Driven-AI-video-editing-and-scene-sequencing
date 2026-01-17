let scenesData = [];
let videosData = [];

// Wizard State
let currentStep = 1;

// Clear inputs on load
window.onload = function() {
    document.getElementById("script-input").value = "";
    if(document.getElementById("script-text-area")) document.getElementById("script-text-area").value = "";
    document.getElementById("video-input").value = "";
    // Attach listener for manual text
    const textArea = document.getElementById('script-text-area');
    if(textArea) {
        textArea.addEventListener('blur', handleScriptText);
        // Also allow Ctrl+Enter to submit
        textArea.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && (e.keyCode === 13 || e.keyCode === 10)) {
                handleScriptText();
            }
        });
    }
    document.querySelectorAll('.wizard-step').forEach(step => {
        if(step.id !== 'step-1') step.classList.remove('active');
        else step.classList.add('active');
    });
};

function showStep(stepNumber) {
    document.querySelectorAll('.wizard-step').forEach(step => {
        step.classList.remove('active');
    });
    
    document.getElementById('step-' + stepNumber).classList.add('active');
    
    // Update Progress Bar (Now 4 Steps)
    const percent = (stepNumber / 4) * 100;
    document.getElementById('progress-bar').style.width = percent + "%";
    
    currentStep = stepNumber;
}

function nextStep(stepNumber) {
    if (stepNumber === 2) {
        if (scenesData.length === 0) return alert("Please upload a script first!");
    }
    if (stepNumber === 3) {
        if (videosData.length === 0) return alert("Please upload at least one video!");
    }
    
    showStep(stepNumber);
}

// File Handlers (Same as before)
async function handleScriptSelect() {
    const input = document.getElementById("script-input");
    const file = input.files[0];
    if (!file) { input.value = ""; return; }
    
    document.getElementById("script-label").innerText = "Analyzing " + file.name + "...";
    
    const formData = new FormData();
    formData.append("script", file);
    
    const preview = document.getElementById("script-preview");
    preview.classList.remove("hidden");
    preview.innerHTML = "<p>Scanning script...</p>";
    
    try {
        const res = await fetch("/upload_script", { method: "POST", body: formData });
        const data = await res.json();
        
        if (data.scenes) {
            scenesData = data.scenes;
            preview.innerHTML = "<h3>✅ Found " + scenesData.length + " Scenes</h3><ul class='scene-list'>" + 
                scenesData.map((s, i) => "<li><span style='color:var(--accent-color)'>Scene " + (i+1) + ":</span> <strong>" + s.header + "</strong></li>").join("") + "</ul>";
            document.getElementById("btn-step1-next").disabled = false;
        } else {
            console.error(data.error);
            preview.innerHTML = "<p style='color: #ff4d4d'>Error: " + data.error + "</p>";
        }
    } catch(e) {
        console.error(e);
        preview.innerHTML = "<p style='color: #ff4d4d'>Error: " + e + "</p>";
    } finally { input.value = ""; }
}

async function handleScriptText() {
    const text = document.getElementById("script-text-area").value;
    if (!text.trim()) return;
    
    const preview = document.getElementById("script-preview");
    preview.classList.remove("hidden");
    preview.innerHTML = "<p>Analyzing text...</p>";
    
    const formData = new FormData();
    formData.append("script_text", text);
    
    try {
        const res = await fetch("/upload_script", { method: "POST", body: formData });
        const data = await res.json();
        
        if (data.scenes) {
            scenesData = data.scenes;
            preview.innerHTML = "<h3>✅ Found " + scenesData.length + " Scenes (Manual Entry)</h3><ul class='scene-list'>" + 
                scenesData.map((s, i) => "<li><span style='color:var(--accent-color)'>Scene " + (i+1) + ":</span> <strong>" + s.header + "</strong></li>").join("") + "</ul>";
            document.getElementById("btn-step1-next").disabled = false;
        } else {
            preview.innerHTML = "<p style='color: #ff4d4d'>Error: " + data.error + "</p>";
        }
    } catch(e) {
        preview.innerHTML = "<p style='color: #ff4d4d'>Error: " + e + "</p>";
    }
}


async function handleVideoSelect() {
    const input = document.getElementById("video-input");
    const files = input.files;
    if (files.length === 0) { input.value = ""; return; }
    
    document.getElementById("video-label").innerText = "Uploading " + files.length + " files...";
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("videos", files[i]);
    }
    
    const preview = document.getElementById("video-preview");
    preview.classList.remove("hidden");
    preview.innerHTML = "<p>Uploading footage...</p>";
    
    try {
        const res = await fetch("/upload_videos", { method: "POST", body: formData });
        const data = await res.json();
        
        if (data.video_paths) {
            videosData = data.video_paths;
            preview.innerHTML = "<h3>✅ " + videosData.length + " Clips Ready</h3>" + 
                                "<p style='color: var(--text-color)'>Matched to your scenes.</p>";
            document.getElementById("btn-step2-next").disabled = false;
        } else {
            console.error(data.error);
            preview.innerHTML = "<p style='color: #ff4d4d'>Error: " + data.error + "</p>";
        }
    } catch(e) {
        console.error(e);
        preview.innerHTML = "<p style='color: #ff4d4d'>Error: " + e + "</p>";
    } finally { input.value = ""; }
}

// Generation with Preferences and Logs
async function generateEdit() {
    const btn = document.getElementById("generate-btn");
    const loading = document.getElementById("loading");
    const display = document.getElementById("output-result");
    const logOutput = document.getElementById("log-output");
    
    // Get Director's Settings
    const mood = document.getElementById("pref-mood").value;
    const pacing = document.getElementById("pref-pacing").value;
    
    
    btn.style.display = "none";
    loading.classList.remove("hidden");
    display.innerHTML = "";
    
    // Fake Log Animation
    const logs = [
        "[ScriptModule] Analyzing narrative structure...",
        "[DirectorEngine] Applying mood: " + mood.toUpperCase() + "...",
        "[DirectorEngine] Adjusting pacing: " + pacing.toUpperCase() + "...",
        "[MatchingEngine] Calculating confidence scores...",
        "[CompositionModule] Rendering final cut..."
    ];
    
    let logIndex = 0;
    const logInterval = setInterval(() => {
        if(logIndex < logs.length) {
            logOutput.innerText += "\n" + logs[logIndex];
            logIndex++;
        }
    }, 800);
    
    const payload = {
        scenes: scenesData,
        video_paths: videosData,
        preferences: { mood: mood, pacing: pacing }
    };
    
    try {
        const res = await fetch("/generate", { 
            method: "POST", 
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        
        clearInterval(logInterval);
        const data = await res.json();
        
        if (data.video_url) {
            const timestamp = new Date().getTime();
            const vUrl = data.video_url + "?t=" + timestamp;
            const confidence = data.confidence_score || 88; // Default to 88 if not sent
            
            display.innerHTML = "<h3>🎬 Your Edit is Ready:</h3>" +
            "<div style='border: 1px solid var(--accent-glow); padding: 5px; border-radius: 8px; box-shadow: 0 0 20px var(--accent-glow); margin-bottom: 1rem;'>" +
            "<video controls src='" + vUrl + "' width='100%' style='border-radius: 4px;'></video>" +
            "</div>" +
            
            // AI Confidence Badge
            "<div style='display: flex; gap: 1rem; justify-content: center; margin-bottom: 1rem;'>" +
            "<div style='background: rgba(0, 255, 157, 0.1); padding: 0.5rem 1rem; border-radius: 20px; color: var(--success-color); border: 1px solid var(--success-color);'>" +
            "🤖 AI Confidence: <strong>" + confidence + "%</strong></div>" +
            "<div style='background: rgba(255, 255, 255, 0.1); padding: 0.5rem 1rem; border-radius: 20px; color: #fff;'>" +
            "mood: " + mood + "</div>" +
            "</div>" +
            
            "<a href='" + vUrl + "' download class='btn btn-primary'>Download Final Cut</a>";
            
        } else {
            console.error("Generation Error:", data.error);
            display.innerHTML = "<p style='color: #ff4d4d; font-weight: bold;'>Error: " + (data.error || "Unknown error") + "</p>";
        }
    } catch(e) {
        console.error("Generation Exception:", e);
        display.innerHTML = "<p style='color: #ff4d4d; font-weight: bold;'>Error: " + e.message + "</p>";
        clearInterval(logInterval);
    } finally {
        btn.style.display = "inline-block";
        loading.classList.add("hidden");
    }
}


