# dashboard_carros_futuristicos.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configurações
np.random.seed(42)
n_carros = 1000

print("🚀 Gerando dataset de carros futurísticos...")

# MODELOS FUTURÍSTICOS
modelos = [
    'Tesla Cybertruck X', 'Lucid Air Sapphire', 'Rimac C_Two', 'Pininfarina Battista',
    'Koenigsegg Gemera', 'Bugatti Bolide', 'Aspark Owl', 'Hennessey Venom F5',
    'Tesla Roadster 2.0', 'Mercedes EQXX', 'Xiaomi SU7 Max', 'BYD Yangwang U9'
]

tipos = ['Elétrico', 'Híbrido', 'Combustão', 'Hidrogênio']
cores = ['Prata', 'Preto', 'Branco', 'Vermelho', 'Azul', 'Verde Neon']

# GERAÇÃO DO DATASET PRINCIPAL
data = {
    'id_veiculo': range(1, n_carros + 1),
    'modelo': np.random.choice(modelos, n_carros, p=[0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.10, 0.08, 0.05, 0.05]),
    'tipo': np.random.choice(tipos, n_carros, p=[0.45, 0.25, 0.20, 0.10]),
    'ano': np.random.choice([2023, 2024, 2025], n_carros, p=[0.2, 0.5, 0.3]),
    'cor': np.random.choice(cores, n_carros),
    'preco_usd': np.random.normal(250000, 80000, n_carros),
    'quilometragem': np.random.exponential(15000, n_carros),
    'potencia_hp': np.random.normal(800, 300, n_carros),
}

df_carros = pd.DataFrame(data)
df_carros['id_veiculo'] = df_carros['id_veiculo'].astype(str)

# CÁLCULOS IMPORTANTES (MÉTRICAS SOLICITADAS)
print("📊 Calculando métricas de performance...")

# Velocidade média (km/h)
df_carros['velocidade_media_kmh'] = np.clip(df_carros['potencia_hp'] * 0.15 + np.random.normal(120, 20, n_carros), 80, 350)

# Consumo de combustível (km/l - adaptado para elétricos como kWh/100km)
df_carros['consumo'] = np.where(
    df_carros['tipo'] == 'Elétrico', 
    np.clip(15 + (df_carros['potencia_hp']/100)*0.8 + np.random.normal(0, 2, n_carros), 12, 25),
    np.clip(8 + np.random.normal(0, 2, n_carros), 5, 15)
)

# Tempo de viagem médio (horas - viagem de 500km)
df_carros['tempo_viagem_h'] = 500 / df_carros['velocidade_media_kmh']

# Performance Score (0-100)
df_carros['performance_score'] = (
    (df_carros['velocidade_media_kmh'] / 300 * 40) +
    (df_carros['consumo'] / 25 * 30) +
    (100 / df_carros['tempo_viagem_h'] * 30)
).clip(0, 100)

# Limpeza de dados
df_carros = df_carros.round(2)
df_carros['preco_usd'] = df_carros['preco_usd'].clip(50000, 3000000)
df_carros['quilometragem'] = df_carros['quilometragem'].clip(0, 100000)

print("✅ Dataset limpo e métricas calculadas!")

# ANÁLISES EXTRAS PARA POWER BI
df_viagens = pd.DataFrame({
    'id_veiculo': np.random.choice(df_carros['id_veiculo'], 5000),
    'data_viagem': pd.date_range('2024-01-01', periods=5000, freq='D') + np.random.randint(0, 365, 5000),
    'distancia_km': np.random.exponential(250, 5000).clip(50, 1000),
    'combustivel_usado': np.random.exponential(20, 5000).clip(5, 80),
    'tempo_real_h': np.random.exponential(3, 5000).clip(0.5, 8)
})

df_viagens = df_viagens.merge(df_carros[['id_veiculo', 'modelo', 'tipo']], on='id_veiculo')

# Métricas agregadas das viagens
df_viagens['velocidade_media_real'] = df_viagens['distancia_km'] / df_viagens['tempo_real_h']
df_viagens['consumo_real'] = df_viagens['combustivel_usado'] / (df_viagens['distancia_km']/100)

# EXPORTAÇÃO DOS ARQUIVOS
df_carros.to_csv('carros_futurísticos.csv', index=False)
df_viagens.to_csv('viagens_carros.csv', index=False)

print("💾 Arquivos exportados:")
print("✅ carros_futurísticos.csv (características)")
print("✅ viagens_carros.csv (viagens detalhadas)")

# VISUALIZAÇÕES RÁPIDAS
plt.style.use('dark_background')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Ranking Performance
top10 = df_carros.nlargest(10, 'performance_score')[['modelo', 'performance_score']]
axes[0,0].barh(range(len(top10)), top10['performance_score'], color='cyan')
axes[0,0].set_yticks(range(len(top10)))
axes[0,0].set_yticklabels(top10['modelo'])
axes[0,0].set_title('🏆 TOP 10 Performance Score')

# Velocidade vs Consumo
sns.scatterplot(data=df_carros, x='velocidade_media_kmh', y='consumo', 
                hue='tipo', size='potencia_hp', ax=axes[0,1], alpha=0.7)
axes[0,1].set_title('⚡ Velocidade vs Consumo por Tipo')

# Distribuição Preço
axes[1,0].hist(df_carros['preco_usd']/1000, bins=30, color='gold', alpha=0.7)
axes[1,0].set_xlabel('Preço (mil USD)')
axes[1,0].set_title('💰 Distribuição de Preços')

# Performance por Tipo
sns.boxplot(data=df_carros, x='tipo', y='performance_score', ax=axes[1,1])
axes[1,1].set_title('📈 Performance por Tipo de Carro')

plt.tight_layout()
plt.savefig('preview_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

print("🎨 Preview salvo como 'preview_dashboard.png'")
print("\n🚀 PRONTO PARA POWER BI! 📊")