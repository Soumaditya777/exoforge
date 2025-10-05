document.addEventListener('DOMContentLoaded', () => {
    // --- Mock Simulation Data ---
    const mockExoplanetData = [
        { name: "Kepler-186f", type: "CONFIRMED", data: { period: 129.944, duration: 5.71, depth: 405.3, planet_radius: 1.17, equilibrium_temp: 188, insolation_flux: 0.29, model_snr: 15.1, stellar_temp: 3754, stellar_logg: 4.59, stellar_radius: 0.54 } },
        { name: "TRAPPIST-1e", type: "CONFIRMED", data: { period: 6.10, duration: 1.22, depth: 733.8, planet_radius: 0.92, equilibrium_temp: 251, insolation_flux: 0.66, model_snr: 102.8, stellar_temp: 2559, stellar_logg: 5.22, stellar_radius: 0.12 } },
        { name: "Proxima Centauri b", type: "CONFIRMED", data: { period: 11.186, duration: 0.95, depth: 520.0, planet_radius: 1.07, equilibrium_temp: 234, insolation_flux: 0.65, model_snr: 25.4, stellar_temp: 3042, stellar_logg: 5.20, stellar_radius: 0.15 } },
        { name: "KOI-7923.01", type: "CANDIDATE", data: { period: 395.29, duration: 8.32, depth: 621.5, planet_radius: 0.99, equilibrium_temp: 219, insolation_flux: 0.98, model_snr: 22.6, stellar_temp: 5780, stellar_logg: 4.45, stellar_radius: 0.98 } },
        { name: "KOI-4878.01", type: "CANDIDATE", data: { period: 449.02, duration: 12.45, depth: 924.1, planet_radius: 1.04, equilibrium_temp: 257, insolation_flux: 1.05, model_snr: 45.9, stellar_temp: 6031, stellar_logg: 4.41, stellar_radius: 1.02 } },
        { name: "KOI-1686.01", type: "CANDIDATE", data: { period: 202.4, duration: 6.9, depth: 1450.7, planet_radius: 3.8, equilibrium_temp: 350, insolation_flux: 4.2, model_snr: 55.2, stellar_temp: 5560, stellar_logg: 4.1, stellar_radius: 1.3 } },
        { name: "HD 100546 b", type: "CANDIDATE", data: { period: 91322, duration: 200, depth: 800, planet_radius: 6.9, equilibrium_temp: 200, insolation_flux: 0.05, model_snr: 12.3, stellar_temp: 6778, stellar_logg: 4.2, stellar_radius: 1.8 } },
        { name: "HD 219134 b", type: "CONFIRMED", data: { period: 3.09, duration: 2.1, depth: 210.5, planet_radius: 1.6, equilibrium_temp: 1015, insolation_flux: 224, model_snr: 30.1, stellar_temp: 4699, stellar_logg: 4.6, stellar_radius: 0.78 } },
        { name: "Kepler-452b", type: "CANDIDATE", data: { period: 384.84, duration: 10.4, depth: 250.2, planet_radius: 1.63, equilibrium_temp: 265, insolation_flux: 1.1, model_snr: 18.7, stellar_temp: 5757, stellar_logg: 4.32, stellar_radius: 1.11 } },
        { name: "Gliese 581g", type: "CANDIDATE", data: { period: 36.56, duration: 3.1, depth: 300, planet_radius: 1.5, equilibrium_temp: 226, insolation_flux: 0.35, model_snr: 15, stellar_temp: 3494, stellar_logg: 4.9, stellar_radius: 0.29 } },
        { name: "KIC 9832227", type: "FALSE_POSITIVE", data: { period: 0.45, duration: 3.5, depth: 42000, planet_radius: 15.2, equilibrium_temp: 2800, insolation_flux: 650, model_snr: 800, stellar_temp: 5800, stellar_logg: 4.0, stellar_radius: 2.5 } },
        { name: "KOI-5", type: "FALSE_POSITIVE", data: { period: 18.2, duration: 4.8, depth: 12500, planet_radius: 12, equilibrium_temp: 950, insolation_flux: 150, model_snr: 350, stellar_temp: 6200, stellar_logg: 4.2, stellar_radius: 1.9 } },
        { name: "Algol", type: "FALSE_POSITIVE", data: { period: 2.87, duration: 9.8, depth: 85000, planet_radius: 3.0, equilibrium_temp: 1200, insolation_flux: 450, model_snr: 2500, stellar_temp: 12500, stellar_logg: 3.8, stellar_radius: 3.2 } },
        { name: "Kepler-20b", type: "CONFIRMED", data: { period: 3.7, duration: 1.9, depth: 359, planet_radius: 1.91, equilibrium_temp: 1040, insolation_flux: 250, model_snr: 40, stellar_temp: 5466, stellar_logg: 4.5, stellar_radius: 0.96 } },
        { name: "Kepler-62f", type: "CONFIRMED", data: { period: 267.29, duration: 7.2, depth: 198.8, planet_radius: 1.41, equilibrium_temp: 208, insolation_flux: 0.41, model_snr: 14.1, stellar_temp: 4925, stellar_logg: 4.5, stellar_radius: 0.64 } },
        { name: "LHS 1140 b", type: "CONFIRMED", data: { period: 24.74, duration: 2.3, depth: 1420, planet_radius: 1.73, equilibrium_temp: 230, insolation_flux: 0.46, model_snr: 25.9, stellar_temp: 3131, stellar_logg: 4.89, stellar_radius: 0.21 } },
        { name: "55 Cancri e", type: "CONFIRMED", data: { period: 0.74, duration: 1.8, depth: 360, planet_radius: 1.88, equilibrium_temp: 2040, insolation_flux: 2500, model_snr: 98.2, stellar_temp: 5196, stellar_logg: 4.5, stellar_radius: 0.94 } },
        { name: "KOI-7711.01", type: "CANDIDATE", data: { period: 173.4, duration: 5.5, depth: 320, planet_radius: 2.0, equilibrium_temp: 300, insolation_flux: 2.1, model_snr: 19.8, stellar_temp: 5890, stellar_logg: 4.4, stellar_radius: 1.05 } },
        { name: "KOI-812.03", type: "FALSE_POSITIVE", data: { period: 0.837, duration: 2.31, depth: 80200, planet_radius: 34.74, equilibrium_temp: 2801, insolation_flux: 8911.3, model_snr: 511.1, stellar_temp: 5853, stellar_logg: 4.45, stellar_radius: 0.96 } },
        { name: "Kepler-10c", type: "CONFIRMED", data: { period: 45.29, duration: 7.0, depth: 330, planet_radius: 2.35, equilibrium_temp: 504, insolation_flux: 10.7, model_snr: 25.1, stellar_temp: 5627, stellar_logg: 4.4, stellar_radius: 1.06 } }
    ];

    // --- Get all DOM elements ---
    const landingPage = document.getElementById('landing-page'), mainAppPage = document.getElementById('main-app-page');
    const initSystemBtn = document.getElementById('init-system-btn');
    const configAiBtn = document.getElementById('config-ai-btn'), runAnalysisBtn = document.getElementById('run-analysis-btn'), retrainBtn = document.getElementById('retrain-btn');
    const configModal = document.getElementById('config-modal'), predictForm = document.getElementById('predict-form');
    const modelAccuracyEl = document.getElementById('model-accuracy');
    const resultsPlaceholder = document.getElementById('results-placeholder'), resultsContent = document.getElementById('results-content');
    const verdictText = document.getElementById('verdict-text'), verdictConfidence = document.getElementById('verdict-confidence');
    const dataEchoList = document.getElementById('data-echo-list');
    const probabilityCanvas = document.getElementById('probability-chart');
    const analysisLog = document.getElementById('analysis-log');
    let probabilityChart;

    // --- Elements for Presets Modal ---
    const loadPresetBtn = document.getElementById('load-preset-btn');
    const presetsModal = document.getElementById('presets-modal');
    const closePresetsBtn = document.getElementById('close-presets-btn');
    const presetsList = document.getElementById('presets-list');

    // --- Function to populate the presets list in the modal ---
    function populatePresets() {
        mockExoplanetData.forEach((planet, index) => {
            const item = document.createElement('div');
            item.className = 'preset-item';
            item.dataset.index = index;
            
            let typeClass = '';
            if (planet.type === 'CONFIRMED') typeClass = 'type-confirmed';
            else if (planet.type === 'CANDIDATE') typeClass = 'type-candidate';
            else typeClass = 'type-fp';

            item.innerHTML = `<strong>${planet.name}</strong> <span class="${typeClass}">(${planet.type.replace('_', ' ')})</span>`;
            presetsList.appendChild(item);
        });
    }

    // --- Event listener to load data when a preset is clicked ---
    presetsList.addEventListener('click', (e) => {
        const item = e.target.closest('.preset-item');
        if (!item) return;

        const selectedIndex = item.dataset.index;
        const planetData = mockExoplanetData[selectedIndex].data;

        for (const key in planetData) {
            const inputElement = document.getElementById(key);
            if (inputElement) {
                inputElement.value = planetData[key];
            }
        }
        presetsModal.classList.add('hidden');
    });

    particlesJS.load('particles-js', '/static/particles.json', () => console.log('Particles.js config loaded.'));
    populatePresets();

    // --- Navigation & Modal Logic ---
    const goToPage = (pageToShow) => {
        console.log(`Navigating to: ${pageToShow.id}`);
        [landingPage, mainAppPage].forEach(p => p.classList.remove('active'));
        pageToShow.classList.add('active');
    };
    
    if (initSystemBtn) {
        initSystemBtn.addEventListener('click', () => goToPage(mainAppPage));
    } else {
        console.error('CRITICAL: "Initialize System" button not found.');
    }

    const closeModalBtn = document.querySelector('#config-modal .close-btn');
    const toggleConfigModal = (show) => configModal.classList.toggle('hidden', !show);
    const togglePresetsModal = (show) => presetsModal.classList.toggle('hidden', !show);
    
    configAiBtn.addEventListener('click', () => { fetchModelStatus(); toggleConfigModal(true); });
    closeModalBtn.addEventListener('click', () => toggleConfigModal(false));

    loadPresetBtn.addEventListener('click', () => togglePresetsModal(true));
    closePresetsBtn.addEventListener('click', () => togglePresetsModal(false));
    
    async function fetchModelStatus() { try { const res = await fetch('/status'), data = await res.json(); modelAccuracyEl.textContent = `Accuracy: ${data.accuracy}`; } catch (e) { modelAccuracyEl.textContent = 'Accuracy: Error'; } }
    
    predictForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        runAnalysisBtn.textContent = 'Analyzing...'; runAnalysisBtn.disabled = true;
        const features = {};
        predictForm.querySelectorAll('input').forEach(input => {
            if (input.value) features[input.id] = parseFloat(input.value);
        });
        try {
            const res = await fetch('/predict', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(features) });
            if (!res.ok) throw new Error(`Server error: ${res.statusText}`);
            const result = await res.json();
            displayResults(result, features);
        } catch (error) { 
            analysisLog.innerHTML = `<p class="log-error">Analysis failed: ${error.message}</p>`;
            alert(`Analysis failed: ${error.message}`);
        } finally { 
            runAnalysisBtn.textContent = 'Run Analysis'; 
            runAnalysisBtn.disabled = false; 
        }
    });
    runAnalysisBtn.addEventListener('click', () => predictForm.requestSubmit());

    function displayResults(result, features) {
        resultsPlaceholder.classList.add('hidden');
        resultsContent.classList.remove('hidden');
        setTimeout(() => resultsContent.classList.add('visible'), 50);
        
        const predictionClass = result.prediction.replace(/ /g, '-');
        verdictText.textContent = result.prediction;
        verdictText.className = predictionClass;

        let confidenceKey;
        if (result.prediction === 'CONFIRMED EXOPLANET') {
            confidenceKey = 'CONFIRMED';
        } else if (result.prediction === 'FALSE POSITIVE') {
            confidenceKey = 'FALSE_POSITIVE';
        } else {
            confidenceKey = 'CANDIDATE';
        }
        const confidenceValue = result.confidence[confidenceKey];
        verdictConfidence.textContent = `${(confidenceValue * 100).toFixed(1)}%`;
        
        dataEchoList.innerHTML = '';
        for (const [key, value] of Object.entries(features)) {
            const li = document.createElement('li');
            li.innerHTML = `<span>${key.replace(/_/g, ' ')}</span><strong>${value}</strong>`;
            dataEchoList.appendChild(li);
        }
        
        analysisLog.innerHTML = `<p>Initializing analysis...</p>
                                 <p>Input data packet validated.</p>
                                 <p>Sending data to ExoForge AI core...</p>
                                 <p>Model processing complete.</p>
                                 <p class="log-success">Verdict received: ${result.prediction}</p>`;

        drawProbabilityChart(probabilityCanvas, result.confidence);
    }
    
    function drawProbabilityChart(canvas, probabilities) {
        if (!canvas) {
            console.error("Probability chart canvas not found!");
            return;
        }
        const labels = ['Confirmed', 'Candidate', 'False Positive'];
        const data = [
            probabilities.CONFIRMED || 0,
            probabilities.CANDIDATE || 0,
            probabilities.FALSE_POSITIVE || 0
        ];
        
        if (probabilityChart) probabilityChart.destroy();
        
        probabilityChart = new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [ 'rgba(63, 185, 80, 0.7)', 'rgba(210, 153, 34, 0.7)', 'rgba(248, 81, 73, 0.7)' ],
                    borderColor: [ '#3fb950', '#d29922', '#f85149' ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#8b949e',
                            boxWidth: 20,
                            font: { family: "'Roboto Mono', monospace" }
                        }
                    }
                }
            }
        });
    }
});