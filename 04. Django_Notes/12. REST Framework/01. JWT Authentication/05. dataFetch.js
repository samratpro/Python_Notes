
// Login Request **********************
function getLogin(username, password, sendResponse){
    const loginData = {
        username: username,
        password: password
    };
    fetch(loginUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed with status: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        const token = data.access;
        if (!token) {
            throw new Error('Token not found in response');
        }
        // Save token to chrome.storage
        chrome.storage.session.set({ authToken: token }, () => console.log('Token saved to storage:'));
        sendResponse({status:'success', token:token})
    })
    .catch(error => {
        console.log('Error during login:', error);
        sendResponse({ status: 'fail', data: error.toString() });
    });
    // Return true to indicate that sendResponse will be called asynchronously
    return true;
}


// Post requst with access token and query parameter **************************
function getData(token, Query, sendResponse){
    fetch(getSiteUrl, 
        { method: 'POST', 
        headers: { 'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'Query-Parameter': Query
                }
                })
    .then(res=>{
      if(!res.ok){
        throw new Error('Response Fail, Error Status: ', res.status)
      }
      return res.json()
    })
    .then(data=>{
        chrome.storage.local.set({ siteList: data }, () => console.log('Token saved to storage:'));
        sendResponse({ status: 'success', data: data})
    })
    .catch(error=>{
        console.log('Error during get site data:', error);
        sendResponse({ status: 'fail', data: error.toString()})
    })
    return true
}
