import React, { useState, useEffect } from 'react';
import { Layout, Card, Row, Col, Statistic, Spin } from 'antd';
import {
  RiseOutlined,
  UserOutlined,
  ShoppingCartOutlined,
  HeartOutlined
} from '@ant-design/icons';
import SalesForecasting from './SalesForecasting';
import CustomerSegmentation from './CustomerSegmentation';
import SentimentAnalysis from './SentimentAnalysis';
import ChurnPrediction from './ChurnPrediction';
import { apiService } from '../services/apiService';
import './Dashboard.css';

const { Header, Content } = Layout;

const Dashboard = () => {
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await apiService.getDashboardOverview();
      setOverview(data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <Layout className="dashboard-layout">
      <Header className="dashboard-header">
        <h1>AI-Powered Business Insights Dashboard</h1>
      </Header>
      
      <Content className="dashboard-content">
        {/* KPI Cards */}
        <Row gutter={[16, 16]} className="kpi-row">
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Revenue"
                value={overview?.total_revenue || 0}
                prefix="$"
                valueStyle={{ color: '#3f8600' }}
                suffix={<RiseOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Active Customers"
                value={overview?.active_customers || 0}
                valueStyle={{ color: '#1890ff' }}
                suffix={<UserOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Orders"
                value={overview?.total_orders || 0}
                valueStyle={{ color: '#722ed1' }}
                suffix={<ShoppingCartOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Customer Satisfaction"
                value={overview?.satisfaction_score || 0}
                suffix="%"
                valueStyle={{ color: '#eb2f96' }}
                prefix={<HeartOutlined />}
              />
            </Card>
          </Col>
        </Row>

        {/* Analytics Sections */}
        <Row gutter={[16, 16]} className="analytics-row">
          <Col xs={24} lg={12}>
            <SalesForecasting />
          </Col>
          <Col xs={24} lg={12}>
            <CustomerSegmentation />
          </Col>
        </Row>

        <Row gutter={[16, 16]} className="analytics-row">
          <Col xs={24} lg={12}>
            <SentimentAnalysis />
          </Col>
          <Col xs={24} lg={12}>
            <ChurnPrediction />
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default Dashboard;