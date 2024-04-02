// api.js
const BASE_URL = 'http://localhost:8000'; // Adjust as necessary for your environment

async function registerUser(user) {
    const response = await fetch('http://localhost:8000/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    });
  
    const data = await response.json();
  
    if (!response.ok) {
      throw new Error(data.detail || 'An error has occurred');
    }
  
    return data;
  }

export { registerUser };
