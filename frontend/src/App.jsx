import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

function App() {
  const [dados, setDados] = useState({});
  const [estacoes, setEstacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      setLoading(true);
      const [dadosResponse, estacoesResponse] = await Promise.all([
        axios.get('/api/dados'),
        axios.get('/api/estacoes')
      ]);
      setDados(dadosResponse.data);
      setEstacoes(estacoesResponse.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar dados: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatarData = (dataStr) => {
    const data = new Date(dataStr);
    return data.toLocaleDateString('pt-BR');
  };

  if (loading) {
    return <div className="loading">Carregando dados...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🌊 Projeto Rio Amazonas - Dashboard</h1>
        <button onClick={carregarDados} className="refresh-btn">
          Atualizar Dados
        </button>
      </header>

      <main className="main">
        {estacoes.map(estacao => (
          <section key={estacao} className="estacao-section">
            <h2>Estação: {estacao}</h2>

            {dados[estacao] && dados[estacao].length > 0 ? (
              <>
                <div className="tabela-container">
                  <table className="dados-tabela">
                    <thead>
                      <tr>
                        <th>Data</th>
                        <th>Vazão (m³/s)</th>
                        <th>Cota (m)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {dados[estacao].map((item, index) => (
                        <tr key={index}>
                          <td>{formatarData(item.data)}</td>
                          <td>{item.vazao ? item.vazao.toFixed(0) : '-'}</td>
                          <td>{item.cota_m ? item.cota_m.toFixed(2) : '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="graficos-container">
                  {dados[estacao].some(item => item.vazao) && (
                    <div className="grafico">
                      <h3>Vazão</h3>
                      <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={dados[estacao]}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis
                            dataKey="data"
                            tickFormatter={formatarData}
                          />
                          <YAxis />
                          <Tooltip labelFormatter={formatarData} />
                          <Legend />
                          <Line
                            type="monotone"
                            dataKey="vazao"
                            stroke="#8884d8"
                            name="Vazão (m³/s)"
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  )}

                  {dados[estacao].some(item => item.cota_m) && (
                    <div className="grafico">
                      <h3>Cota</h3>
                      <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={dados[estacao]}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis
                            dataKey="data"
                            tickFormatter={formatarData}
                          />
                          <YAxis />
                          <Tooltip labelFormatter={formatarData} />
                          <Legend />
                          <Line
                            type="monotone"
                            dataKey="cota_m"
                            stroke="#82ca9d"
                            name="Cota (m)"
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <p className="sem-dados">Sem dados disponíveis para esta estação</p>
            )}
          </section>
        ))}
      </main>
    </div>
  );
}

export default App;