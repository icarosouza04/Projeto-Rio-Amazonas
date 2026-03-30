import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

function App() {
  const [dados, setDados] = useState({});
  const [estacoes, setEstacoes] = useState([]);
  const [estacaoSelecionada, setEstacaoSelecionada] = useState('');
  const [periodo, setPeriodo] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const periodosDisponiveis = [
    { label: 'Todos os dados', value: 0 },
    { label: 'Últimos 7 dias', value: 7 },
    { label: 'Últimos 30 dias', value: 30 },
    { label: 'Últimos 90 dias', value: 90 },
    { label: 'Últimos 180 dias', value: 180 },
    { label: 'Último ano', value: 365 }
  ];

  useEffect(() => {
    if (!estacaoSelecionada && estacoes.length > 0) {
      setEstacaoSelecionada(estacoes[0]);
      return;
    }

    if (estacaoSelecionada) {
      carregarDados(estacaoSelecionada, periodo);
    }
  }, [estacoes, estacaoSelecionada, periodo]);

  const carregarDados = async (estacao = '', dias = 0) => {
    try {
      setLoading(true);
      const [estacoesResponse] = await Promise.all([axios.get('/api/estacoes')]);
      setEstacoes(estacoesResponse.data?.estacoes || []);
      if (!estacao && estacoesResponse.data?.estacoes?.length > 0) {
        estacao = estacoesResponse.data.estacoes[0];
        setEstacaoSelecionada(estacao);
      }

      const params = {};
      if (estacao) params.estacao = estacao;
      if (dias > 0) params.dias = dias;

      const dadosResponse = await axios.get('/api/dados', { params });
      setDados(dadosResponse.data);
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
        <section className="filtros-section">
          <label>
            Estação:
            <select value={estacaoSelecionada} onChange={(e) => setEstacaoSelecionada(e.target.value)}>
              {estacoes.map((estacao) => (
                <option key={estacao} value={estacao}>{estacao}</option>
              ))}
            </select>
          </label>

          <label>
            Período:
            <select value={periodo} onChange={(e) => setPeriodo(Number(e.target.value))}>
              {periodosDisponiveis.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>

          <button onClick={() => carregarDados(estacaoSelecionada, periodo)} className="refresh-btn">
            Aplicar filtro
          </button>
        </section>

        <section className="estacao-section">
          <h2>Estação: {estacaoSelecionada || 'Nenhuma selecionada'}</h2>

          {estacaoSelecionada && dados[estacaoSelecionada] && dados[estacaoSelecionada].dados && dados[estacaoSelecionada].dados.length > 0 ? (
            <>
              <div className="meta">
                <p>Fonte de dados: {dados[estacaoSelecionada].fonte || 'desconhecida'}</p>
              </div>

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
                    {dados[estacaoSelecionada].dados.map((item, index) => (
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
                {dados[estacaoSelecionada].dados.some(item => item.vazao) && (
                  <div className="grafico">
                    <h3>Vazão</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={dados[estacaoSelecionada].dados}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="data" tickFormatter={formatarData} />
                        <YAxis />
                        <Tooltip labelFormatter={formatarData} />
                        <Legend />
                        <Line type="monotone" dataKey="vazao" stroke="#8884d8" name="Vazão (m³/s)" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}

                {dados[estacaoSelecionada].dados.some(item => item.cota_m) && (
                  <div className="grafico">
                    <h3>Cota</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={dados[estacaoSelecionada].dados}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="data" tickFormatter={formatarData} />
                        <YAxis />
                        <Tooltip labelFormatter={formatarData} />
                        <Legend />
                        <Line type="monotone" dataKey="cota_m" stroke="#82ca9d" name="Cota (m)" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>

              {dados[estacaoSelecionada].tendencia_mensal && Object.keys(dados[estacaoSelecionada].tendencia_mensal).length > 0 && (
                <div className="tendencia-section">
                  <h3>Tendência Mensal (média cota)</h3>
                  <ul>
                    {Object.entries(dados[estacaoSelecionada].tendencia_mensal).map(([mes, valor]) => (
                      <li key={mes}>{mes}: {valor.toFixed(2)} m</li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <p className="sem-dados">Sem dados disponíveis para esta estação com o período selecionado.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;