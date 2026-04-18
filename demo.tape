Output demo.gif

Set Shell "bash"
Set FontSize 13
Set Width 1000
Set Height 520
Set Theme "Dracula"
Set Padding 20
Set PlaybackSpeed 1.0

Hide
Type "cd /home/user/api-skill-creator"
Enter
Show

Sleep 400ms

Type "cat output/stripe/api_spec.json | python3 skills/skill-creator/scripts/generate_skill.py --name stripe --output /tmp/stripe-skill --force"
Sleep 600ms
Enter
Sleep 3s

Type "python3 /tmp/stripe-skill/scripts/stripe_cli.py --help"
Sleep 600ms
Enter
Sleep 2s

Type "python3 /tmp/stripe-skill/scripts/stripe_cli.py charges --help"
Sleep 600ms
Enter
Sleep 2s
