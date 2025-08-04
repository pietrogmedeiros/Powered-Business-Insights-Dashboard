import React, { useState, useEffect } from 'react';
import { Card, Spin, Alert, Table, Tag, Progress } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiService } from '../services/apiService';

const ChurnPrediction = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadChurnData();
  }, []);

  const loadChurnData = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.getChurnPrediction();
      setData(result);
    } catch (err) {
      setError('Failed to load churn prediction data');
      console.error('Error loading churn:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'High': return 'red';
      case 'Medium': return 'orange';
      case 'Low': return 'green';
      default: return 'default';
    }
  };

  const columns = [
    {
      title: 'Customer ID',
      dataIndex: 'customer_id',
      key: 'customer_id',
      width: 120,
    },
    {
      title: 'Churn Risk',
      dataIndex: 'churn_probability',
      key: 'churn_probability',
      render: (value) => (
        <Progress 
          percent={Math.round(value * 100)} 
          size="small" 
          status={value > 0.7 ? 'exception' : value > 0.3 ? 'active' : 'success'}
        />
      ),
      width: 150,
    },
    {
      title: 'Risk Level',
      dataIndex: 'risk_level',
      key: 'risk_level',
      render: (level) => (
        <Tag color={getRiskColor(level)}>{level}</Tag>
      ),
      width: 100,
    },
  ];

  const formatFeatureImportance = () => {
    if (!data?.feature_importance) return [];
    
    return data.feature_importance.slice(0, 5).map(item => ({
      feature: item.feature.replace('_', ' ').toUpperCase(),
      importance: Math.round(item.importance * 100)
    }));
  };

  if (loading) {
    return (
      <Card title="Churn Prediction" style={{ height: 400 }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Churn Prediction" style={{ height: 400 }}>
        <Alert message={error} type="error" />
      </Card>
    );
  }

  return (
    <Card title="Churn Prediction" style={{ height: 400 }}>
      <div style={{ display: 'flex', height: 300 }}>
        <div style={{ flex: 1 }}>
          <h4>Top At-Risk Customers</h4>
          <Table
            dataSource={data?.churn_predictions?.slice(0, 8) || []}
            columns={columns}
            pagination={false}
            size="small"
            rowKey="customer_id"
            scroll={{ y: 200 }}
          />
        </div>
        
        <div style={{ flex: 1, paddingLeft: 16 }}>
          <h4>Feature Importance</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={formatFeatureImportance()} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="feature" type="category" width={80} />
              <Tooltip />
              <Bar dataKey="importance" fill="#1890ff" />
            </BarChart>
          </ResponsiveContainer>
          
          <div style={{ marginTop: 16 }}>
            <p><strong>Overall Churn Rate:</strong> {(data?.churn_rate * 100 || 0).toFixed(1)}%</p>
          </div>
        </div>
      </div>
      
      {data?.insights && (
        <div style={{ marginTop: 16 }}>
          <h4>Key Insights:</h4>
          <ul>
            {data.insights.map((insight, index) => (
              <li key={index}>{insight}</li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
};

export default ChurnPrediction;