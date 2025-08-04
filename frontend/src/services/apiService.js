import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      timeout: 30000,
    });
  }

  async getDashboardOverview() {
    const response = await this.api.get('/dashboard/overview');
    return response.data;
  }

  async getSalesForecasting(periods = 30) {
    const response = await this.api.get(`/forecast/sales?periods=${periods}`);
    return response.data;
  }

  async getCustomerSegmentation() {
    const response = await this.api.get('/segmentation/customers');
    return response.data;
  }

  async getSentimentAnalysis() {
    const response = await this.api.get('/sentiment/analysis');
    return response.data;
  }

  async getChurnPrediction() {
    const response = await this.api.get('/churn/prediction');
    return response.data;
  }

  async retrainModels() {
    const response = await this.api.post('/models/retrain');
    return response.data;
  }
}

export const apiService = new ApiService();