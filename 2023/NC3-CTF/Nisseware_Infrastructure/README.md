Continuing from the OSINT chall, we have to look further.

This time, sadly Sherlock cannot help us. But we can use our own skills! N1ss3f4r talks about using old social media.. hmm..

We checked MySpace etc., and after a while we find his Instagram profile: https://www.instagram.com/n1ss3f4r/

On that, we find a screenshot that shows the login credentials to the challenge server: https://www.instagram.com/p/CzvOfbJMy51/

We get in and find the first part of the flag `NC3{N1ss3b4nd3ns_53rv3r`.

From the mail in the instagram post, it mentions that the server runs some tasks automatically, interesting.

We find this crontab `/5 * * * root /bin/bash /root/run_all.sh /usr/scheduled`.

In `/usr/scheduled` we find bash scripts which are run as root - and luckily we can add new files to this folder!

I let my other teammate take it over from here to do some boot2root by having the script run `chmod +s /bin/bash`, and boom, we're in as root.

And with this we get the full flag: `NC3{N1ss3b4nd3ns_53rv3r_1nf1ltr3r3t_g00d_j0b!}`
