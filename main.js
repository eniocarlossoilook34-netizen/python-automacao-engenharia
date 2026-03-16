import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

// --- 1. CONFIGURAÇÕES E ESTADO ---
const simConfig = {
    velocity: 10,
    aoa: 0,
    viscosity: 0.000015,
};

let scene, camera, renderer, cube, velocityArrow;
let particles; 
const particleCount = 500; 
const particleData = []; 
let vortexStrengths = []; // Armazena a matriz de gammas vinda do Python

// --- 2. CONFIGURAÇÃO DO GRÁFICO (CHART.JS) ---
let performanceChart;
const chartData = {
    labels: [],
    datasets: [{
        label: 'Cl (Sustentação)',
        data: [],
        borderColor: '#58a6ff',
        backgroundColor: 'rgba(88, 166, 255, 0.1)',
        borderWidth: 2,
        tension: 0.3,
        fill: true
    }]
};

// --- 3. INICIALIZAÇÃO DAS STREAMLINES ---
function initStreamlines() {
    const geo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
        const x = Math.random() * 10 - 5;
        const y = Math.random() * 4 - 2;
        const z = (Math.random() - 0.5) * 1.5;

        positions[i * 3] = x;
        positions[i * 3 + 1] = y;
        positions[i * 3 + 2] = z;

        particleData.push({ ox: x, oy: y, oz: z });
    }

    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.03, transparent: true, opacity: 0.6 });
    particles = new THREE.Points(geo, mat);
    scene.add(particles);
}

// --- 4. MOTOR 3D (PERFIL NACA CORRIGIDO) ---
function init3D() {
    scene = new THREE.Scene();
    const backgroundGeo = new THREE.SphereGeometry(100, 32, 32);
    const backgroundMat = new THREE.MeshBasicMaterial({ color: 0x1e272e, side: THREE.BackSide });
    scene.add(new THREE.Mesh(backgroundGeo, backgroundMat));

    camera = new THREE.PerspectiveCamera(75, 400 / 250, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(400, 250);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    const points = [];
    const segments = 60;
    const chord = 2.0; 
    const t = 0.12; 

    for (let i = 0; i <= segments; i++) {
        let x = i / segments;
        let yt = 5 * t * (0.2969 * Math.sqrt(x) - 0.1260 * x - 0.3516 * Math.pow(x, 2) + 0.2843 * Math.pow(x, 3) - 0.1015 * Math.pow(x, 4));
        points.push(new THREE.Vector2(x * chord - chord/2, yt));
    }
    for (let i = segments; i >= 0; i--) {
        let x = i / segments;
        let yt = 5 * t * (0.2969 * Math.sqrt(x) - 0.1260 * x - 0.3516 * Math.pow(x, 2) + 0.2843 * Math.pow(x, 3) - 0.1015 * Math.pow(x, 4));
        points.push(new THREE.Vector2(x * chord - chord/2, -yt));
    }

    const shape = new THREE.Shape(points);
    const geometry = new THREE.ExtrudeGeometry(shape, { depth: 1.5, bevelEnabled: false });
    geometry.center(); 
    geometry.rotateY(Math.PI / 2); 

    const material = new THREE.MeshStandardMaterial({ color: 0x58a6ff, metalness: 0.8, roughness: 0.2 });
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    const light = new THREE.DirectionalLight(0xffffff, 1.5);
    light.position.set(5, 5, 5);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));

    camera.position.set(0, 0.5, 3.5);
    camera.lookAt(0, 0, 0);
}

// --- 5. GRÁFICO E UI ---
function initChart() {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    performanceChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: '#30363d' }, ticks: { color: '#8b949e' } },
                x: { grid: { color: '#30363d' }, ticks: { color: '#8b949e' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

const inputs = { velocity: document.getElementById('velocity'), aoa: document.getElementById('aoa') };
const displays = { velocity: document.getElementById('val-v'), aoa: document.getElementById('val-aoa') };

function logStatus(message) {
    const now = new Date().toLocaleTimeString();
    document.getElementById('status-display').innerHTML = `[${now}] ${message}`;
}

function updateSimulation() {
    simConfig.velocity = parseFloat(inputs.velocity.value);
    simConfig.aoa = parseFloat(inputs.aoa.value);
    displays.velocity.innerText = simConfig.velocity;
    displays.aoa.innerText = simConfig.aoa;

    if (cube) {
        cube.rotation.x = (simConfig.aoa * Math.PI) / 180;
        updateVelocityArrow(); 
    }
}

function updateVelocityArrow() {
    if (velocityArrow) scene.remove(velocityArrow);
    const length = simConfig.velocity * 0.05;
    velocityArrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), new THREE.Vector3(-2.5, 0, 0), length, 0x39ff14, 0.2, 0.1);
    scene.add(velocityArrow);
}

// --- 6. COMUNICAÇÃO COM O BACKEND (VORTEX PANEL METHOD) ---
document.getElementById('run-simulation').addEventListener('click', async () => {
    logStatus("Enviando para motor Python (Vortex Panel Solver)...");
    try {
        const response = await fetch('http://127.0.0.1:8000/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(simConfig)
        });
        const result = await response.json();
        if (result.status === "success") {
            document.getElementById('stat-re').innerText = result.reynolds;
            document.getElementById('stat-cl').innerText = result.cl;
            
            // CAPTURA A MATRIZ DE INFLUÊNCIA (GAMMAS)
            vortexStrengths = result.gammas; 

            chartData.labels.push(`${simConfig.aoa}°`);
            chartData.datasets[0].data.push(result.cl);
            if (chartData.labels.length > 10) { chartData.labels.shift(); chartData.datasets[0].data.shift(); }
            performanceChart.update();
            logStatus("Matriz de Influência resolvida com sucesso.");
        }
    } catch (error) { logStatus("Erro: Motor Python Offline."); }
});

// --- 7. LOOP DE ANIMAÇÃO COM SUPERPOSIÇÃO DE PAINÉIS ---
function animate() {
    requestAnimationFrame(animate);

    if (particles) {
        const positions = particles.geometry.attributes.position.array;
        const alpha = (simConfig.aoa * Math.PI) / 180;
        const vx_inf = simConfig.velocity * 0.003; 

        for (let i = 0; i < particleCount; i++) {
            let px = positions[i * 3];
            let py = positions[i * 3 + 1];

            let v_ind_x = 0;
            let v_ind_y = 0;

            // SUPERPOSIÇÃO FÍSICA: Se houver dados da matriz, cada painel influencia a partícula
            if (vortexStrengths.length > 0) {
                vortexStrengths.forEach((gamma_val, idx) => {
                    // Distribui os centros de vórtice ao longo da corda (-1 a 1)
                    let x_panel = -1 + (idx * (2.0 / vortexStrengths.length));
                    let dx = px - x_panel;
                    let dy = py - (x_panel * Math.tan(alpha));
                    let rSq = dx * dx + dy * dy + 0.8; // Kernel de suavização (soft-core)

                    // Lei de Biot-Savart para cada elemento da matriz
                    v_ind_x += (gamma_val * dy) / (2 * Math.PI * rSq);
                    v_ind_y -= (gamma_val * dx) / (2 * Math.PI * rSq);
                });
            } else {
                // Fallback físico simples enquanto o botão não é clicado
                const gamma_global = 2 * Math.PI * vx_inf * Math.sin(alpha);
                const rSq = px * px + py * py + 0.15;
                v_ind_x = (gamma_global * py) / (2 * Math.PI * rSq);
                v_ind_y = -(gamma_global * px) / (2 * Math.PI * rSq);
            }

            // Atualiza posição: U_total = U_inf + Soma das Velocidades Induzidas
            positions[i * 3] += vx_inf + v_ind_x;
            positions[i * 3 + 1] += v_ind_y;

            // Restrição de Colisão (Fronteira Sólida NACA)
            if (px > -1.0 && px < 1.0) {
                const x_norm = (px + 1) / 2;
                const yt = 0.5 * (0.2969 * Math.sqrt(x_norm) - 0.1260 * x_norm - 0.3516 * Math.pow(x_norm, 2));
                const surfaceY = (py > 0 ? 1 : -1) * yt + (px * Math.tan(alpha));
                
                if (py > 0 && py < surfaceY) positions[i * 3 + 1] = surfaceY + 0.04;
                if (py < 0 && py > surfaceY) positions[i * 3 + 1] = surfaceY - 0.04;
            }

            // Reset das partículas
            if (positions[i * 3] > 5) {
                positions[i * 3] = -5;
                positions[i * 3 + 1] = particleData[i].oy;
            }
        }
        particles.geometry.attributes.position.needsUpdate = true;
    }
    renderer.render(scene, camera);
}

// Inicialização Final
inputs.velocity.addEventListener('input', updateSimulation);
inputs.aoa.addEventListener('input', updateSimulation);
init3D();
initChart();
initStreamlines(); 
updateVelocityArrow();
animate();