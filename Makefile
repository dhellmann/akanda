LIB = akanda
UNAME := $(shell uname)
DEV_DIR = ~/lab/DreamHost/dhc
PYPF_DIR = $(DEV_DIR)/pypf
TXROUTES_DIR = $(DEV_DIR)/txroutes
AKANDA_DIR = $(DEV_DIR)/akanda
PYPF_INSTALL = /usr/local/lib/python2.7/site-packages/pypf
PYPF_URL = git@github.com:dreamhost/pypf.git
TXROUTES_URL = git@github.com:dreamhost/txroutes.git
AKANDA_URL = git@github.com:dreamhost/akanda.git
USER = oubiwann
PYTHON = /usr/local/bin/python
GIT = /usr/local/bin/git
TWISTD = /usr/local/bin/twistd
PF_HOST ?= 10.0.4.186
PF_HOST_UNAME = $(shell ssh root@$(PF_HOST) "uname")

clean:
	sudo rm -rfv dist/ build/ MANIFEST *.egg-info
	rm -rfv _trial_temp/ CHECK_THIS_BEFORE_UPLOAD.txt twistd.log
	find ./ -name "*~" -exec rm -v {} \;
	sudo find ./ -name "*.py[co]" -exec rm -v {} \;
	find . -name "*.sw[op]" -exec rm -v {} \;

system-setup:
	pw user mod $(USER) -G wheel

install-ports:
	portsnap fetch
	portsnap extract

update-ports:
	portsnap fetch
	portsnap update

$(PYTHON):
ifeq ($(UNAME), FreeBSD)
	cd /usr/ports/lang/python && make install clean
endif
ifeq ($(UNAME), OpenBSD)
	pkg_add -i python
endif

$(GIT):
ifeq ($(UNAME), FreeBSD)
	cd /usr/ports/devel/git && make install clean
endif
ifeq ($(UNAME), OpenBSD)
	pkg_add -i git
endif

$(TWISTD):
ifeq ($(UNAME), FreeBSD)
	cd /usr/ports/devel/py-twisted && make install clean
endif
ifeq ($(UNAME), OpenBSD)
	pkg_add -i py-twisted-core
	pkg_add -i py-twisted-web
endif

$(DEV_DIR):
	mkdir -p $(DEV_DIR)

$(PYPF_DIR):
	-cd $(DEV_DIR) && git clone $(PYPF_URL)

$(PYPF_INSTALL): $(DEV_DIR) $(PYPF_DIR)
	cd $(PYPF_DIR) && python setup.py install

$(TXROUTES_DIR):
	cd $(DEV_DIR) && git clone $(TXROUTES_URL)

$(TXROUTES_INSTALL): $(DEV_DIR) $(TXROUTES_DIR)
	cd $(TXROUTES_DIR) && python setup.py install

python-deps: $(TWISTD) $(PYPF_INSTALL) $(TXROUTES_INSTALL)

install-dev: $(PYTHON) $(GIT) python-deps
ifeq ($(UNAME), FreeBSD)
	@echo "Be sure you have pf enabled on your system:"
	@echo " * edit your /etc/rc.conf"
	@echo " * add rules to /etc/pf.conf"
	@echo " * start pf: sudo /etc/rc.d/pf start"
	@echo
	@echo "To use the dev targets, you will need to edit your"
	@echo "/etc/ssh/sshd_config to allow remote login for root"
	@echo "and then you'll need to restart ssh:"
	@echo "  /etc/rc.d/sshd restart"
	@echo
endif

local-dev-deps:
ifeq ($(PF_HOST_UNAME), FreeBSD)
	ssh root@$(PF_HOST) "cd /usr/ports/net/rsync && make install clean"
endif
ifeq ($(PF_HOST_UNAME), OpenBSD)
	ssh root@$(PF_HOST) "pkg_add -i rsync"
endif

clone-dev:
	git push
	-ssh root@$(PF_HOST) \
	"git clone $(AKANDA_URL) $(AKANDA_DIR)"

push-dev: clone-dev
	git push
	ssh root@$(PF_HOST) \
	"cd $(AKANDA_DIR) && git pull && python setup.py install"

rsync-push-dev: local-dev-deps
	rsync -az -e "ssh . root@$(PF_HOST):$(AKANDA_DIR)/"

scp-push-dev:
	scp -r . root@$(PF_HOST):$(AKANDA_DIR)/
	ssh root@$(PF_HOST) \
	"cd $(AKANDA_DIR) && python setup.py install"

check-dev: push-dev
	ssh root@$(PF_HOST) "cd $(AKANDA_DIR) && python -c \
	'from akanda import scripts;scripts.run_all()'"

check:
	trial $(LIB)
