/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'manhvgt.uk.auth0.com', // the auth0 domain prefix
    audience: 'drinks', // the audience set for the auth0 app
    clientId: '3OhFrm0ok2zaxxlP8IhOPkh75bC8uKTP', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:5000/drinks', // the base url of the running ionic application. 
  }
};
