# Fastapi-exchangeRates
<p align="center">
  <img src="https://media.giphy.com/media/d2Z12G5H3wAjPpkI/giphy.gif">
</p>
<h2> 🎯 Main Target </h2>
<p> First of all, programm should dedicate account of the user. There two types of account -> first is administrator, second is cashier. Likewise, after dedication -> administrator must accept or reject worker.<b> Consider the case number one you're enter cashier account.</b> Thereafter, cashier can choose where he/she 'll be work & which currency. All work done, now you can withdraw to buy or sell currency. Nevertheless, you can unload history document. Settings, also available, here you can change username & password.<b> Consider the case number two you're enter administrator account.</b> Here open more capabilities, adm. can abserve history of the each worker. </p>
<p align="center">
  <img src="https://sun9-26.userapi.com/impg/BKWU11ABXlCj-xpP_Pj6vijXxZtxk72SC75UQQ/UgmQeDLg3Js.jpg?size=604x580&quality=96&sign=d3c47d957af570dfee16c2c320cb1952&type=album">
</p>
<p> When I started talk with my potential clien He doesnt like this behaviour & we decided that we makes it. a week passed, the customer brought what he needed, I finalized it and that's what happened. I can’t show the whole mechanism that he described - it’s confidential, but it’s easy to catch my train of thought on the development of the project!</p>
<p align="center">
  <img src="https://sun9-68.userapi.com/impg/86rsCQS5tlXCUOyxbxPXJsnxvWrP7luFgqbccA/kCeC96jivsA.jpg?size=1475x461&quality=96&sign=2555b0d4a0092ac08fa19a399a8715f4&type=album">
</p>
<p> I decided to work with Fastapi systeam. I thought it was interesting then, and the opportunity to learn a new framework did not frighten me at all. I created <code> main.py </code> & with some basic structors beggin' work. I started to build the meaning of the pages and make them visualized to make it easier to understand what's what, while I stopped there. However, he soon continued and began to write each time under the code in the form of a TODO comment. It helped me not to forget what was happening and what I needed to add. For example, in the registration window, attach to postgresql.  </p>
<p align="center">
  <img src="https://sun9-81.userapi.com/impg/NyhXYBVcFZcxrdAnRAAAoi5LAEuOn7veiPuy1w/KJ0u2iYUkwI.jpg?size=1920x1080&quality=96&sign=8e766bea8ab7dc5870e679aa2108ef93&type=album">
</p>
<p align="center">
  <img src="https://sun9-50.userapi.com/impg/RDlX_yGhA80e35-EdqlCbUNkJpWyzCIBtGNDDA/XdJW09RfkzY.jpg?size=1920x1080&quality=96&sign=8f145b5000551ac80f0df3b52aa1b572&type=album">
</p>
<p> Excellent, currently i decided to test it on the real server & deploy it! in case you need help with remote downloading to github page <code> https://oiplug.com/blog/git/5049/ </code> </p>
<code> https://server-exchangerates.herokuapp.com/ </code>
<h1> FastAPI-Authentication </h1>
Authentication in fastapi app
<p align="center">
  <img src="https://media.giphy.com/media/Wb6fHuJCH7zELdsqSn/giphy.gif">
</p>
<p> Test projct for detect how work authentification system on fastapi. Open terminal <code> sqlite3 users.db </code>, than type <code> SELECT * FROM users; </code>. Received result is your database on the server </p>
<h2> 👤 Registration & Login </h2>
<p> <b>What is Role based Access Control (RBAC)</b> - Most of the CRUD apps, require some level of role based access control.

You may have at least two types of users.

Elevated permission user (admin, root or superuser)
Normal user aka everyone else ;)
More likely you have more levels in between.

This means only the users with specific role can access certain API endpoints or operations e.g. Allow everyone the GET operation, but only admin can DELETE. Some levels in-between can create/update etc.
</p>
<p> 
  <code>What does init_auth do?</code>
init_auth fetches metadata from PropelAuth that it will use to verify users. It does this once on startup, so that it can verify users without making any external requests.
<p align="center">
  <img src="https://sun9-48.userapi.com/impg/FeNv_5uofNToTrmTLzoPswXASz2cjbdR1KbETw/JhbAVhdDm8Q.jpg?size=1830x1030&quality=96&sign=01f390fbd9c5c61e09a8ad6e50459c25&type=album">
</p>
  <code>How does require_user work?</code>
When your frontend makes a request to the backend, it will include a token for the user that made the request. require_user verifies this token (using the metadata it fetched in init_auth), and injects the User into the request. If invalid credentials are provided, the request is rejected.

  <code>What is an org_id?</code>
It's an identifier for an organization. PropelAuth provides B2B authentication meaning that your users can create organizations, invite their coworkers to join them, and manage roles within the organization.
</p>
<p align="center">
  <img src="https://media.giphy.com/media/O8IpEOGKM40PoNtT3h/giphy.gif">
</p>

