import React from 'react';
import { motion } from 'framer-motion';

const FloatingLogCard = ({ log, index }) => {
  const isAnomaly = log.anomaly === 1;
  
  // Randomize floating parameters for each card to create a natural "zero gravity" feel
  const randomDelay = Math.random() * 2;
  const randomDuration = 3 + Math.random() * 4;
  const randomX = (Math.random() - 0.5) * 20;
  const randomRotate = (Math.random() - 0.5) * 5;

  const anomalyVariants = {
    float: {
      y: [0, -30, 0],
      x: [0, randomX * 2, 0],
      rotate: [randomRotate, -randomRotate * 2, randomRotate],
      transition: {
        duration: randomDuration / 1.5,
        repeat: Infinity,
        ease: "easeInOut",
        delay: randomDelay
      }
    },
    shake: {
      x: [0, -2, 2, -2, 2, 0],
      transition: {
        duration: 0.4,
        repeat: Infinity,
      }
    }
  };

  const normalVariants = {
    float: {
      y: [0, -15, 0],
      x: [0, randomX, 0],
      rotate: [randomRotate, -randomRotate, randomRotate],
      transition: {
        duration: randomDuration,
        repeat: Infinity,
        ease: "easeInOut",
        delay: randomDelay
      }
    }
  };

  return (
    <motion.div
      className={`log-card glass-card ${isAnomaly ? 'log-anomaly' : 'log-normal'}`}
      initial={{ opacity: 0, scale: 0.8, y: 50 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ scale: 1.05, zIndex: 10 }}
    >
      <motion.div 
        className={`glow-overlay ${isAnomaly ? 'glow-red' : 'glow-blue'}`}
        animate={{ opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
      
      <motion.div
        variants={isAnomaly ? anomalyVariants : normalVariants}
        animate={isAnomaly ? ["float", "shake"] : "float"}
      >
        <div className={`log-badge ${isAnomaly ? 'badge-anomaly' : 'badge-normal'}`}>
          {isAnomaly ? 'Anomaly Detected' : 'Normal'}
        </div>
        <div style={{ color: isAnomaly ? '#fca5a5' : '#7dd3fc', marginBottom: '0.5rem' }}>
          {isAnomaly ? '[CRITICAL_ERR]' : '[SYS_LOG]'}
        </div>
        <div style={{ lineHeight: 1.4 }}>
          {log.Content}
        </div>
      </motion.div>
    </motion.div>
  );
};

const FloatingLogs = ({ logs }) => {
  if (!logs || logs.length === 0) return null;

  return (
    <div className="logs-container">
      {logs.map((log, index) => (
        <FloatingLogCard key={index} log={log} index={index} />
      ))}
    </div>
  );
};

export default FloatingLogs;
