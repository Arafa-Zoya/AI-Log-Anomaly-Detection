import React from 'react';
import { motion } from 'framer-motion';
import { Activity, ShieldAlert, FileText } from 'lucide-react';

const StatCard = ({ label, value, icon: Icon, color }) => (
  <motion.div 
    className="glass-card stat-card"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    whileHover={{ y: -5, boxShadow: `0 0 20px ${color}33` }}
  >
    <Icon size={24} color={color} style={{ marginBottom: '1rem' }} />
    <div className="stat-label">{label}</div>
    <motion.div 
      className="stat-value"
      initial={{ scale: 0.5 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 100 }}
    >
      {value}
    </motion.div>
  </motion.div>
);

const Dashboard = ({ stats }) => {
  return (
    <div className="dashboard-grid">
      <StatCard 
        label="Total Logs Scanned" 
        value={stats.total} 
        icon={FileText} 
        color="#38bdf8" 
      />
      <StatCard 
        label="Anomalies Detected" 
        value={stats.anomalies} 
        icon={ShieldAlert} 
        color="#ef4444" 
      />
      <StatCard 
        label="Health Status" 
        value={stats.total > 0 ? (stats.anomalies > 0 ? "WARNING" : "SECURE") : "WAITING"} 
        icon={Activity} 
        color={stats.anomalies > 0 ? "#ef4444" : "#22c55e"} 
      />
    </div>
  );
};

export default Dashboard;
