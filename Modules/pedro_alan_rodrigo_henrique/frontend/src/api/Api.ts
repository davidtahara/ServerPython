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
}
