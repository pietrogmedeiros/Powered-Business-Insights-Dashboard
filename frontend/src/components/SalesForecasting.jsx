import React, { useState, useEffect } from 'react';
import { Card, Spin, Select, Alert } from 'antd';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiService } from '../services/apiService';

const { Option } = Select;

const SalesForecasting = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [periods, setPeriods] = useState(30);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadForecastData();
  }, [periods]);

  const loadForecastData = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.getSalesForecasting(periods);
      setData(result);
    } catch (err) {
      setError('Failed to load sales forecast data');
      console.error('Error loading forecast:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatChartData = () => {
    if (!data?.forecast) return [];
    
    return data.forecast.map(item => ({
      date: new Date(item.ds).toLocaleDateString(),
      predicted: Math.round(item.yhat),
      lower: Math.round(item.yhat_lower),
      upper: Math.round(item.yhat_upper)
    }));
  };

  if (loading) {
    return (
      <Card title="Sales Forecasting" style={{ height: 400 }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Sales Forecasting" style={{ height: 400 }}>
        <Alert message={error} type="error" />
      </Card>
    );
  }

  return (
    <Card 
      title="Sales Forecasting" 
      extra={
        <Select value={periods} onChange={setPeriods} style={{ width: 120 }}>
          <Option value={7}>7 days</Option>
          <Option value={30}>30 days</Option>
          <Option value={90}>90 days</Option>
        </Select>
      }
      style={{ height: 400 }}
    >
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={formatChartData()}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip formatter={(value) => [`$${value}`, 'Sales']} />
          <Legend />
          <Line type="monotone" dataKey="predicted" stroke="#1890ff" strokeWidth={2} name="Predicted Sales" />
          <Line type="monotone" dataKey="lower" stroke="#ff7875" strokeDasharray="5 5" name="Lower Bound" />
          <Line type="monotone" dataKey="upper" stroke="#52c41a" strokeDasharray="5 5" name="Upper Bound" />
        </LineChart>
      </ResponsiveContainer>
      
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

export default SalesForecasting;