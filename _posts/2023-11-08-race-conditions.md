---
layout: post
title: Race Conditions in Mastodon posting
date: 2023-11-08 05:16
---
Yes there are race conditions when GitHub actions posts on Mastodon like it can abort the build midway too and that is really annoying but the essential effect is that it posts on Mastodon THEN it uploads the post and this whole race condition is making the previews break and that is NOT something that should happen but there is like a few seconds of limbo where the post is posted then the post exists and this would be bad for many reasons not only previews but also stuff like IndexNow and yeah *Mweeoops*
