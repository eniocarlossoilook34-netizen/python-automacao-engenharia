import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm

# --- 1. CONFIGURAÇÃO IGUAL AO ANTERIOR ---
nx, ny = 81, 41
nt = 500         # Total de frames da física
nit = 50         # Iterações da pressão
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
rho = 1
nu = 0.1
dt = .001

u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx)) 
b = np.zeros((ny, nx))

# Funções auxiliares (mesmas de antes)
def build_up_b(b, rho, dt, u, v, dx, dy):
    b[1:-1, 1:-1] = (rho * (1 / dt * ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx) + 
                     (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
                    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 -
                    2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
                         (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) -
                    ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2))
    return b

def pressure_poisson(p, dx, dy, b):
    pn = np.empty_like(p)
    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 + 
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
                          (2 * (dx**2 + dy**2)) -
                          dx**2 * dy**2 / (2 * (dx**2 + dy**2)) * b[1:-1, 1:-1])
        p[:, -1] = p[:, -2]
        p[0, :] = p[1, :]
        p[-1, :] = p[-2, :]
        p[:, 0] = p[:, 1]
    return p

# --- 2. LISTA PARA GUARDAR OS "FRAMES" ---
snapshots_para_video = []

print("🌪️ Calculando a Física (Aguarde a barra de progresso)...")

# --- 3. LOOP DE SIMULAÇÃO ---
for n in tqdm(range(nt)):
    un = u.copy()
    vn = v.copy()
    b = build_up_b(b, rho, dt, u, v, dx, dy)
    p = pressure_poisson(p, dx, dy, b)
    
    u[1:-1, 1:-1] = (un[1:-1, 1:-1]- un[1:-1, 1:-1] * dt / dx * (un[1:-1, 1:-1] - un[1:-1, 0:-2]) - vn[1:-1, 1:-1] * dt / dy * (un[1:-1, 1:-1] - un[0:-2, 1:-1]) - dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, 0:-2]) + nu * (dt / dx**2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) + dt / dy**2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))
    v[1:-1, 1:-1] = (vn[1:-1, 1:-1] - un[1:-1, 1:-1] * dt / dx * (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) - vn[1:-1, 1:-1] * dt / dy * (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) - dt / (2 * rho * dy) * (p[2:, 1:-1] - p[0:-2, 1:-1]) + nu * (dt / dy**2 * (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1]) + dt / dx**2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2])))

    # Condições de Contorno
    u[:, 0], v[:, 0] = 1, 0
    u[:, -1], v[:, -1] = u[:, -2], v[:, -2]
    u[0, :], u[-1, :], v[0, :], v[-1, :] = 0, 0, 0, 0
    
    # OBSTÁCULO
    u[15:25, 30:40] = 0
    v[15:25, 30:40] = 0
    
    # --- O SEGREDO DO GIF ---
    # Só salvamos a cada 5 passos para o GIF não ficar gigante e demorado
    if n % 5 == 0:
        # Calculamos a Magnitude (Velocidade Total)
        magnitude = np.sqrt(u**2 + v**2)
        snapshots_para_video.append(magnitude.copy())

# --- 4. GERANDO O GIF ---
print("🎥 Física concluída! Renderizando o vídeo (Isso pode levar um minuto)...")

fig = plt.figure(figsize=(10, 6))
plt.title("Simulação CFD Navier-Stokes: Velocidade", fontsize=14)
plt.xlabel("X")
plt.ylabel("Y")

# Lista que vai guardar as imagens prontas para o artista do Matplotlib
frames_artisticos = []

for frame_data in snapshots_para_video:
    # Cria a imagem do frame atual
    # 'animated=True' é importante para otimização
    img = plt.imshow(frame_data, cmap='jet', origin='lower', animated=True, vmin=0, vmax=2.0)
    
    # Adicionamos o obstáculo cinza por cima (estático)
    obstaculo = plt.Rectangle((30, 15), 10, 10, color='gray')
    plt.gca().add_patch(obstaculo)
    
    frames_artisticos.append([img, obstaculo])

# Cria a animação
ani = animation.ArtistAnimation(fig, frames_artisticos, interval=50, blit=True, repeat_delay=1000)

# Salva como GIF usando o motor 'Pillow' (que já vem no Python)
ani.save("Navier_Stokes_Animation.gif", writer='pillow', fps=20)

print("🚀 SUCESSO! O arquivo 'Navier_Stokes_Animation.gif' foi salvo na pasta.")