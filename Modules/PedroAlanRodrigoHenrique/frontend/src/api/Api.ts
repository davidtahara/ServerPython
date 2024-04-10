export default class Api {
  private readonly baseUrl: string;
  constructor() {
    this.baseUrl = "http://localhost:8000";
  }

  async get(path: string) {
    const response = await fetch(`${this.baseUrl}${path}`);
    return await response.json();
  }
}
