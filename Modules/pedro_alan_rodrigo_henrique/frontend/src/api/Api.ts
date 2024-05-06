export default class Api {
  private readonly baseUrl: string;
  constructor() {
    this.baseUrl = "http://localhost:3001/grupo_pedro_alan_rodrigo_henrique/ip";
  }

  async get(path: string) {
    const response = await fetch(`${this.baseUrl}${path}`);
    const data = await response.json();
    return data;
  }

  async post(path: string, data?: any) {
    await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  }
}
