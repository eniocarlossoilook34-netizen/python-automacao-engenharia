from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Habilita o CORS para que o JS consiga falar com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimConfig(BaseModel):
    velocity: float
    aoa: float

@app.post("/calculate")
async def calculate_aerodynamics(config: SimConfig):
    try:
        U_inf = config.velocity
        alpha = np.radians(config.aoa)
        
        # 1. DISCRETIZAÇÃO (Matriz de 20 painéis para precisão)
        num_panels = 20
        x = np.linspace(-1, 1, num_panels + 1)
        # Pontos de controle (centro dos painéis)
        x_c = 0.5 * (x[1:] + x[:-1])
        
        # 2. MONTAGEM DA MATRIZ DE INFLUÊNCIA [A]
        # Baseado na Teoria de Perfil Fino (Thin Airfoil Theory)
        A = np.zeros((num_panels, num_panels))
        for i in range(num_panels):
            for j in range(num_panels):
                if i == j:
                    A[i, j] = 1.0 # Termo de auto-influência
                else:
                    A[i, j] = 1.0 / (x_c[i] - x_c[j])

        # 3. VETOR LADO DIREITO {b} (Condição de contorno: velocidade normal zero)
        # O fluido não atravessa a asa inclinada
        b = 2 * np.pi * U_inf * (alpha - 0.0) # 0.0 seria a inclinação do perfil

        # 4. RESOLUÇÃO DO SISTEMA LINEAR (Onde a mágica acontece)
        # Resolvemos Ax = b para encontrar a intensidade de cada vórtice (gamma)
        gammas = np.linalg.solve(A + np.eye(num_panels)*0.1, np.full(num_panels, b))
        
        # 5. RESULTADOS TÉCNICOS
        cl = 2 * np.pi * alpha  # Teoria Linear para Cl
        reynolds = (U_inf * 2.0) / 1.5e-5 # Corda de 2m, Viscosidade do ar

        return {
            "status": "success",
            "cl": round(float(cl), 4),
            "reynolds": round(float(reynolds), 2),
            "gammas": gammas.tolist(), # Enviando a matriz resolvida para o JS
            "x_coords": x_c.tolist()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)