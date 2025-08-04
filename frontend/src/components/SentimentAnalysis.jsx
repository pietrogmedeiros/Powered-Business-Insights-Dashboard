import React, { useState, useEffect } from 'react';
import { Card, Spin, Alert, Progress, Tag } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { apiService } from '../services/apiService';

const SENTIMENT_COLORS = {
  positive: '#52c41a',
  negative: '#ff4d4f',
  neutral: '#faad14'
};

const SentimentAnalysis = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSentimentData();
  }, []);

  const loadSentimentData = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.getSentimentAnalysis();
      setData(result);
    } catch (err) {
      setError('Failed to load sentiment analysis data');
      console.error('Error loading sentiment:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatPieData = () => {
    if (!data?.sentiment_distribution) return [];
    
    return Object.entries(data.sentiment_distribution).map(([sentiment, value]) => ({
      name: sentiment.charAt(0).toUpperCase() + sentiment.slice(1),
      value: Math.round(value * 100),
      fill: SENTIMENT_COLORS[sentiment]
    }));
  };

  const formatWordData = (words, type) => {
    if (!words || words.length === 0) return [];
    
    return words.slice(0, 5).map(item => ({
      word: item.word,
      score: Math.round(item.score * 100),
      fill: type === 'positive' ? '#52c41a' : '#ff4d4f'
    }));
  };

  if (loading) {
    return (
      <Card title="Sentiment Analysis" style={{ height: 400 }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Sentiment Analysis" style={{ height: 400 }}>
        <Alert message={error} type="error" />
      </Card>
    );
  }

  const positiveWords = formatWordData(data?.top_positive_words, 'positive');
  const negativeWords = formatWordData(data?.top_negative_words, 'negative');

  return (
    <Card title="Sentiment Analysis" style={{ height: 400 }}>
      <div style={{ display: 'flex', height: 300 }}>
        <div style={{ flex: 1 }}>
          <h4>Sentiment Distribution</h4>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={formatPieData()}
                cx="50%"
                cy="50%"
                outerRadius={60}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}%`}
              >
                {formatPieData().map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        <div style={{ flex: 1, paddingLeft: 16 }}>
          <h4>Top Keywords</h4>
          <div style={{ marginBottom: 16 }}>
            <h5 style={{ color: '#52c41a' }}>Positive Words:</h5>
            {positiveWords.map((word, index) => (
              <Tag key={index} color="green" style={{ margin: 2 }}>
                {word.word}
              </Tag>
            ))}
          </div>
          <div>
            <h5 style={{ color: '#ff4d4f' }}>Negative Words:</h5>
            {negativeWords.map((word, index) => (
              <Tag key={index} color="red" style={{ margin: 2 }}>
                {word.word}
              </Tag>
            ))}
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

export default SentimentAnalysis;