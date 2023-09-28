export default {
  name: 'navbar',
  template: `
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" style="color: #7FFFD4;" href="#">THE JOB SEEKER</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="./created_role_listings.html">CREATED POSTING</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">SKILLS</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">EMPLOYEES</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">LOGOUT</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
`,
};