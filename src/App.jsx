import { useEffect, useState } from "react";

function InputSection() {
  const [name, setName] = useState("");
  const [greeting, setGreeting] = useState("");

  function handleClick() {
    fetch("http://localhost:5001/example/hello", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    })
      .then((response) => response.json())
      .then((json) => setGreeting(json.message))
      .catch();
  }

  return (
    <>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name?"
      />
      <button onClick={handleClick}>Submit</button>
      <p>{greeting}</p>
    </>
  );
}

function DatabaseTest() {
  const [fruits, setFruits] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5001/fruits")
      .then(result => result.json())
      .then(json => setFruits(json))
  }, []);

  return (
    <ol>
      {fruits.map(fruit => <li>{fruit.fruit_name}</li>)}
    </ol>
  );
}

function App() {
  const [firstElem, setFirstElem] = useState();
  const [secondElem, setSecondElem] = useState();

  useEffect(() => {
    fetch("http://localhost:5001/example/12")
      .then((response) => response.json())
      .then((json) => {
        setFirstElem(json.firstElem);
        setSecondElem(json.secondElem);
      })
      .catch((_error) => { });
  }, []);

  return (
    <>
      <h1>Example of API</h1>
      <h2>GET example:</h2>
      <ul>
        <li>{firstElem}</li>
        <li>{secondElem}</li>
      </ul>
      <h2>POST example:</h2>
      <InputSection />
      <h2>Database query example:</h2>
      <DatabaseTest />
    </>
  );
}

export default App;
