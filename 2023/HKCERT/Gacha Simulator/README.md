The challenge is a Gacha game in VBA in PowerPoint, which is password protected.

In the hints / steps for this challenge we are provided with this helpful link, which we can use to unlock the file for editing:
https://stackoverflow.com/questions/1026483/is-there-a-way-to-crack-the-password-on-an-excel-vba-project

We unzip the file, get the vbaproject.bin, open in HEX editor, make the key invalid, open Visual Basic to change the key to "hkcert" and reopen. Now we can edit the file.

The first thing we want, is to play more Gacha! So let's change the ticket logic to remove the ticket countdown.

And now we change our luck to be the opposite of what the rates were initially :D

Now when we draw we get-- wait what's this.. oh god why, no, this flag cannot be copied and it scrolls aaaaaaa D:

So, we can change the output to put the encrypted URL as the name instead.. so we get that the flag is.. a website!
https://tar.bz2.top/rr0oy1cq5e62yb3cyvavvhjkpqtrgqqis9lmm7dib5h8oiplxw4px2fpumzuehsx

We can then simply put this website in our browser, open inspect element, and yoink flag is ours now:
hkcert23{FIl1liIIlI1III1lll1IlI11ag_Hmrnmmrnmmmrnmn}
