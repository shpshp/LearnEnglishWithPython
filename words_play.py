#!/usr/bin/python3
import random, sys, codecs, glob

WORDLIST = []
com = ''
EHW = []
RHW = []
VALID_CMD = ['re', 'rr', 'se', 'sr', 'rehw', 'rrhw', 'sehw', 'srhw']
language = ""

HELP = """  ---------------------------------------- HELP MENU ----------------------------------------
  h | help - Print that help menu
  q - Exit to main mode while you are in Random or Sequential word mode
  q | quit - Exit from program

  ehw - Display Current Language Hard Words List
  rhw - Display Current Russian Hard Words List

  fe - Flush Language Hard Words List
  fr - Flush Russian Hard Words List

  m - Mark word as hard word (Add it to corresponding hard words list (Language or Russian))

  r - Refresh words base

  re - Random Language words mode (From Global Language Words List)
  rr - Random Russian words mode (From Global Russian Words List)

  rehw - Random Language hard-words mode (From Language Hard Words List)
  rrhw - Random Russian hard-words mode (From Russian Hard Words List)

  s - Print word count statistics

  se - Sequential Language words mode (From Global Language Words List)
  sr - Sequential Russian words mode (From Global Russian Words List)

  sehw - Sequential Language hard-words mode (From Language Hard Words List)
  srhw - Sequential Russian hard-words mode (From Russian Hard Words List)
  --------------------------------------------------------------------------------------------"""
def umlaut_handler(e):
	part = e.object[e.start:e.end]
	if part == u'ü':
		replacement = u'ue'
	elif part == u'Ü':
		replacement = u'Ue'
	elif part == u'ä':
		replacement = u'ae'
	elif part == u'Ä':
		replacement = u'Ae'
	elif part == u'ö':
		replacement = u'oe'
	elif part == u'Ö':
		replacement = u'Oe'
	elif part == u'ß':
		replacement = u'ss'
	elif part == u'é':
		replacement = u'e'
	else:
		replacement = u'?'
	return replacement, e.start + len(part)

def print_console(line):
	print(str(codecs.encode(line, sys.stdout.encoding, 'umlaut'), sys.stdout.encoding))

def feed():
	L = []
	f1 = open('words_' + language + '.txt', 'a')
	f1.close()
	f1 = open('words_' + language + '.txt', 'r' , encoding = 'utf8')
	for line in f1:
		if (line !='\n'):
			if (' - ' in line):
				L.append(line.split(' - '))
			else:
				print_console('Skipping the line [' + line +']\n')
	f1.close()
	return(L)

def load_hw(prefix):
	L = []
	f1 = open(prefix + language + '.txt', 'a')
	f1.close()
	f1 = open(prefix + language + '.txt', 'r', encoding = 'utf8')
	for line in f1:
		if (line !='\n'):
			L.append(line)
	f1.close()
	return(L)

def load_last_sequential(prefix):
	result = 0
	f1 = open(prefix + language + '.txt', 'a')
	f1.close()
	f1 = open(prefix + language + '.txt', 'r', encoding = 'utf8')
	for line in f1:
		if (line !='\n'):
			result = int(line)
			break
	f1.close()
	return(result)

def save_last_sequential(prefix, value):
	f1 = open(prefix + language + '.txt', 'w', encoding = 'utf8')
	f1.write(value)
	f1.close()

def hw_feed(F):
	if F == 'ehw':
		LL = []
		for line in EHW:
			if (line !='\n'):
				if (' - ' in line):
					LL.append(line.split(' - '))
				else:
					print_console('Skipping the line [' + line +']\n')
		return LL

	if F == 'rhw':
		LL = []
		for line in RHW:
			if (line !='\n'):
				if (' - ' in line):
					LL.append(line.split(' - '))
				else:
					print_console('Skipping the line [' + line +']\n')
	return LL

def boxer(S, i = 0):
	SL = len(str(codecs.encode(S, sys.stdout.encoding, 'umlaut'), sys.stdout.encoding))
	if i == 0:
		print_console('|' + '-'*(SL+2) + '|\n'+'| ' + S + ' |\n' + '|' + '-'*(SL+2) + '|\n')
	else:
		print_console('.' * (i+4) + '|' + '-'*(SL+2) + '|\n' + '.'*(i+4) + '| ' + S + ' |\n' + '.'*(i+4) + '|' + '-'*(SL+2) + '|\n')

def ehw(a,b):
	EHW.append(a.rstrip() + ' - ' + b.rstrip() + '\n')

def rhw(a,b):
	RHW.append(b.rstrip() + ' - ' + a.rstrip() + '\n')

def random_lang(flag = 'e', L = []):
	x = 0
	y = 1
	otstup = 52
	text = 'RANDOM ' + language.upper() + ' WORDS MODE'
	if flag == 'e1':
		text = 'RANDOM ' + language.upper() + ' WORDS FROM HARD WORDS LIST MODE'
		otstup = 41
	if flag == 'r':
		x = 1
		y = 0
		text = 'RANDOM RUSSIAN WORDS MODE'
	if flag == 'r1':
		text = 'RANDOM RUSSIAN WORDS FROM HARD WORDS LIST MODE'
		otstup = 41
	while True:
		K = L[random.randint(0,len(L) - 1)]
		print_console(' '*otstup + '<--------| ' + text + ' |-------->\n')
		print_console('*'*150 + '\n')
		boxer(K[x].rstrip())
		xx = input('')
		if (xx == 'q') or (xx == 'quit'):
			break
		if (xx == 'm') and ((flag == 'e') or (flag == 'e1')):
			ehw(K[x], K[y])
		elif (xx == 'm') and ((flag == 'r') or (flag == 'r1')):
			rhw(K[y], K[x])
		print_console('*' * 150)
		boxer(K[y].rstrip(), len(K[x].rstrip()))
		xxx = input('')
		if (xxx == 'q') or (xxx == 'quit'):
			break
		if (xxx == 'm') and ((flag == 'e') or (flag == 'e1')):
			ehw(K[x], K[y])
		elif (xxx == 'm') and ((flag == 'r') or (flag == 'r1')):
			rhw(K[y], K[x])
		continue

def sequential_lang(flag = 'e', L = []):
	#t0 = 0
	t0 = load_last_sequential('pos_' + flag + '_')
	x = 0
	y = 1
	otstup = 49
	text = language.upper() + ' WORDS BY SEQUENCE'
	if flag == 'e1':
		otstup = 38
		text = language.upper() + ' WORDS BY SEQUENCE FROM HARD WORDS LIST'
	if flag == 'r':
		x = 1
		y = 0
		text = 'RUSSIAN WORDS BY SEQUENCE'
	if flag == 'r1':
		otstup = 38
		text = 'RUSSIAN WORDS BY SEQUENCE FROM HARD WORDS LIST'
	for tt in L:
		print_console(' '*49 + '<---| ' + text + ' -> ' + str(t0 + 1) + ' of ' + str(len(L)) + ' |--->\n')
		t0 += 1
		save_last_sequential('pos_' + flag + '_', str(t0))
		print_console('*'*150 + '\n')
		boxer(tt[x].rstrip())
		xx = input('')
		if (xx == 'q') or (xx == 'quit'):
			break
		if (xx == 'm') and ((flag == 'e') or (flag == 'e1')):
			ehw(tt[x], tt[y])
		elif (xx == 'm') and ((flag == 'r') or (flag == 'r1')):
			rhw(tt[y], tt[x])
		print_console('*' * 150)
		boxer(tt[y].rstrip(), len(tt[x].rstrip()))
		xxx = input('')
		if (xxx == 'q') or (xxx == 'quit'):
			break
		if (xxx == 'm') and ((flag == 'e') or (flag == 'e1')):
			ehw(tt[x], tt[y])
		elif (xxx == 'm') and ((flag == 'r') or (flag == 'r1')):
			rhw(tt[y], tt[x])
		if t0 == len(L):
			print_console('\nALL WORDS ARE FETCHED!\n')
		continue

def mscript(kom):
	if (kom == 're') and (not WORDLIST):
		print_console('Global Word List is empty')
	elif kom == 're':
		print_console(language.upper() + ' words will appear in random order from Global ' + language.upper() + ' Words List\n')
		random_lang('e', WORDLIST)

	if (kom == 'rr') and (not WORDLIST):
		print_console('Global Word List is empty')
	elif kom == 'rr':
		print_console('Russian words will appear in random order from Global Russian Words List\n')
		random_lang('r', WORDLIST)


	if (kom == 'se') and (not WORDLIST):
		print_console('Global Word List is empty')
	elif kom == 'se':
		print_console(language.upper() + ' words will appear sequentially from the Global ' + language.upper() + ' Words base.\n')
		sequential_lang('e', WORDLIST)

	if (kom == 'sr') and (not WORDLIST):
		print_console('Global Word List is empty')
	elif kom == 'sr':
		print_console(language.upper() + ' words will appear sequentially from the Global Russian Words base.\n')
		sequential_lang('r', WORDLIST)


	if (kom == 'rehw') and (not EHW):
		print_console('Currently there is no word(s) added to ' + language.upper() + ' Hard Words list\n')
	elif kom == 'rehw':
		print_console(language.upper() + ' words will appear in random order from the ' + language.upper() + ' Hard Words List.\n')
		L = hw_feed(F = 'ehw')
		random_lang('e1', L)

	if (kom == 'rrhw') and (not RHW):
		print_console('Currently there is no word(s) added to Russian Hard Words list\n')
	elif kom == 'rrhw':
		print_console('Russian words will appear in random order from the Russian Hard Words List.\n')
		L = hw_feed(F = 'rhw')
		random_lang('r1', L)


	if (kom == 'sehw') and (not EHW):
		print_console('Currently there is no word(s) added to ' + language.upper() + ' Hard Words list\n')
	elif kom == 'sehw':
		print_console(language.upper() + ' words will appear sequentially from the ' + language.upper() + ' Hard Words List.\n')
		L = hw_feed(F = 'ehw')
		sequential_lang('e1', L)

	if (kom == 'srhw') and (not RHW):
		print_console('Currently there is no word(s) added to Russian Hard Words list\n')
	elif kom == 'srhw':
		print_console('Russian words will appear sequentially from the Russian Hard Words List.\n')
		L = hw_feed(F = 'rhw')
		sequential_lang('r1',L)

codecs.register_error('umlaut', umlaut_handler)
random.seed()

print_console('\nSupported languages:\n')
for dicfile in glob.glob("words_*.txt"):
    print(dicfile.replace('words_','').replace('.txt',''))

language = input('\nChoose language [q - quit]: ')
print_console('\n')

if (language == 'q') or (language == 'quit'):
    quit()

WORDLIST = feed()
EHW = load_hw('ehw_')
RHW = load_hw('rhw_')

print_console('#'*150 + '\n\n  Welcome to "Word-Practice-Script"! Currently, there are ' + str(len(WORDLIST)) + ' words in our base.\n  Please enter "h" or "help" (without quotes) to list supported commands\' list\n\n'+'#'*150)

###########################################################################################################

while com != 'quit':
	com=input('Enter command: ')
	print_console('\n')

	if (com == 'q') or (com == 'quit'):
		f1 = open('ehw_' + language + '.txt', 'w', encoding = 'utf8')
		for line in EHW:
			f1.write(line)
		f1.close()
		f1 = open('rhw_' + language + '.txt', 'w', encoding = 'utf8')
		for line in RHW:
			f1.write(line)
		f1.close()
		break

	if (com =='r') or (com == 'R'):
		L2 = WORDLIST
		WORDLIST = []
		WORDLIST = feed()
		if L2 == WORDLIST:
			print_console('\nNo changes made to words base!\n')
		else:
			print_console('\nWords Base Refreshed! Now there are ' + str(len(WORDLIST)) + ' words to practice.\n')

	if (com == 's') or (com == 'S'):
		print_console('\nCurrently there are ' + str(len(WORDLIST)) + ' words for practising.\n')
		continue

	if (com == 'h') or (com == 'help'):
		print_console(HELP)

	if com == 'fe':
		EHW = []
		print_console('\n !!! ' + language.upper() + ' HARD WORDS LIST HAS BEEN FLUSHED !!!\n')

	if com == 'fr':
		RHW = []
		print_console('\n !!! RUSSIAN HARD WORDS LIST HAS BEEN FLUSHED !!!\n')

	if com == 'ehw':
		if not EHW:
			print_console(language.upper() + ' Hard Word(s) List is Currently Empty\n')
		else:
			for line in EHW:
				print_console(line)

	if com == 'rhw':
		if not RHW:
			print_console('Russian Hard Word(s) List is Currently Empty\n')
		else:
			for line in RHW:
				print_console(line)

	if com in VALID_CMD:
		mscript(com)

	else:
		continue

###########################################################################################################
