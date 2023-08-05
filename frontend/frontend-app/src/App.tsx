import {useEffect, useState} from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './index.css'
import {AuthenticationContext} from "./service/AuthenticationContext";
import {User} from "./model/UserDataModel";
import {getUser} from "./service/UserAuthenticationService";
import {NavigationButton} from "./components/NavigationButton";
import {NavigationBar} from "./components/NavigationBar";
import {LoginButton} from "./components/LoginButton";

function App() {
    const [count, setCount] = useState(0)
    const [user, setUser] = useState<User>({username: "default", email: "default", valid: false})
    const prefix = "http://localhost:9000";

    function login() {
        void getUser(prefix, setUser).then(
            (result) => {
                if (!result) {
                    window.location.href = prefix + "/oauth"
                }
            })
    }

    function getUserWithoutLogin() {
        void getUser(prefix, setUser).then(
            (result) => {})
    }

    useEffect(() => {
        getUserWithoutLogin();
    }, [])

    console.log(user)

  return (
      <AuthenticationContext.Provider value={user}>
          <>
              <NavigationBar/>
              <div className="flex">
                  <NavigationButton title="Home"/>
                  <LoginButton title={user.valid ? user.username : "Login"} loginFunction={login}/>
              </div>
              <div>
                  <a href="https://vitejs.dev" target="_blank">
                      <img src={viteLogo} className="logo" alt="Vite logo" />
                  </a>
                  <a href="https://react.dev" target="_blank">
                      <img src={reactLogo} className="logo react" alt="React logo" />
                  </a>
              </div>
              <h1>Vite + React + {user.username}</h1>
              <div className="card">
                  <button onClick={() => setCount((count) => count + 1)}>
                      count is {count}
                  </button>
                  <button onClick={() => login()}>
                      Login
                  </button>
                  <p>
                      Edit <code>src/App.tsx</code> and save to test HMR
                  </p>
              </div>
              <p className="read-the-docs">
                  Click on the Vite and React logos to learn more
              </p>
          </>
      </AuthenticationContext.Provider>
  )
}

export default App
