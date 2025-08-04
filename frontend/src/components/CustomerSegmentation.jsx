import React, { useState, useEffect } from 'react';
import { Card, Spin, Alert, Table } from 'antd';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { apiService } from '../services/apiService';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const CustomerSegmentation = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSegmentationData();
  }, []);

  const loadSegmentationData = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.getCustomerSegmentation();
      setData(result);
    } catch (err) {
      setError('Failed to load customer segmentation data');
      console.error('Error loading segmentation:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatPieData = () => {
    if (!data?.segments) return [];
    
    return data.segments.map((segment, index) => ({
      name: segment.description,
      value: segment.size,
      color: COLORS[index % COLORS.length]
    }));
  };

  const columns = [
    {
      title: 'Segment',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Size',
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: 'Avg Revenue',
      dataIndex: 'avg_monetary',
      key: 'avg_monetary',
      render: (value) => `$${value.toFixed(2)}`,
    },
    {
      title: 'Avg Frequency',
      dataIndex: 'avg_frequency',
      key: 'avg_frequency',
      render: (value) => value.toFixed(1),
    },
    {
      title: 'Avg Recency (days)',
      dataIndex: 'avg_recency',
      key: 'avg_recency',
      render: (value) => Math.round(value),
    },
  ];

  if (loading) {
    return (
      <Card title="Customer Segmentation" style={{ height: 400 }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Customer Segmentation" style={{ height: 400 }}>
        <Alert message={error} type="error" />
      </Card>
    );
  }

  return (
    <Card title="Customer Segmentation" style={{ height: 400 }}>
      <div style={{ display: 'flex', height: 300 }}>
        <div style={{ flex: 1 }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={formatPieData()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {formatPieData().map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        <div style={{ flex: 1, paddingLeft: 16 }}>
          <Table
            dataSource={data?.segments || []}
            columns={columns}
            pagination={false}
            size="small"
            rowKey="cluster_id"
          />
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

export default CustomerSegmentation;