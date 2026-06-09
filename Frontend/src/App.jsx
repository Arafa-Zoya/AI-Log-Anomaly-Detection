import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Upload from './components/Upload';
import FloatingLogs from './components/FloatingLogs';
import Dashboard from './components/Dashboard';
import { analyzeLogs } from './services/api';

const BackgroundParticles = () => {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    const newParticles = Array.from({ length: 30 }).map((_, i) => ({
      id: i,
      size: Math.random() * 4 + 1,
      left: Math.random() * 100 + '%',
      top: Math.random() * 100 + '%',
      duration: Math.random() * 20 + 10,
      delay: Math.random() * 5
    }));
    setParticles(newParticles);
  }, []);

  return (
    <div className="background-effects">
      {particles.map(p => (
        <motion.div
          key={p.id}
          className="particle"
          style={{
            width: p.size,
            height: p.size,
            left: p.left,
            top: p.top,
          }}
          animate={{
            y: [-20, -120, -20],
            x: [-20, 20, -20],
            opacity: [0.2, 0.5, 0.2],
          }}
          transition={{
            duration: p.duration,
            repeat: Infinity,
            delay: p.delay,
            ease: "linear"
          }}
        />
      ))}
    </div>
  );
};

function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ total: 0, anomalies: 0 });

  const handleUpload = async (file) => {
    setLoading(true);
    try {
      const data = await analyzeLogs(file);
      setLogs(data.logs);
      
      const anomalyCount = data.logs.filter(l => l.anomaly === 1).length;
      setStats({
        total: data.logs.length,
        anomalies: anomalyCount
      });
    } catch (error) {
      alert("Failed to analyze logs. Make sure the FastAPI server is running at http://127.0.0.1:8000");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <BackgroundParticles />
      
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ textAlign: 'center' }}
      >
        <div className="subtitle">Project Antigravity</div>
        <h1>Log Anomaly Intelligence</h1>
      </motion.div>

      <Dashboard stats={stats} />
      
      <Upload onUpload={handleUpload} loading={loading} />

      <AnimatePresence>
        {logs.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            style={{ width: '100%' }}
          >
            <FloatingLogs logs={logs} />
          </motion.div>
        )}
      </AnimatePresence>
      
      {logs.length === 0 && !loading && (
        <motion.div 
          style={{ marginTop: '4rem', color: '#475569', fontSize: '0.9rem', fontStyle: 'italic' }}
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          Awaiting input stream...
        </motion.div>
      )}
    </div>
  );
}

export default App;
