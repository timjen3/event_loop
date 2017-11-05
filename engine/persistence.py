import pickle
import gzip
import os


class ProgressStore:
	__LOADED_ = dict()

	@classmethod
	def __get_shelf_(cls, inst, uid):
		shelf_location_ = os.sep.join(["_bin", "{}".format(inst.__class__.__name__)])
		bin_name_ = "{}._bin".format(uid)
		full_bin_name = os.sep.join([shelf_location_, bin_name_])

		# ALREADY LOADED, JUST RETURN
		if full_bin_name in cls.__LOADED_:
			return cls.__LOADED_[full_bin_name]

		# IF EXISTS ON DISK, LOAD FROM DISK
		os.makedirs(shelf_location_, exist_ok=True)
		if os.path.exists(full_bin_name):
			with gzip.open(full_bin_name, "rb") as pckl_:
				cls.__LOADED_[full_bin_name] = pickle.load(pckl_)

		# IF NOT FOUND ON DISK, LOAD NEW DICT
		else:
			cls.__LOADED_[full_bin_name] = dict()

		# RETURN REFERENCED DICT
		return cls.__LOADED_[full_bin_name]

	@classmethod
	def sync(cls):
		for file_name_, shlv_ in cls.__LOADED_.items():
			with gzip.open(file_name_, "wb") as pckl_:
				pickle.dump(shlv_, pckl_)

	"""The following methods require an instance of a class (from which the __name__ is pulled to create a dir and
	to serve as part of the unique id... a uid that will distinguish the instance from other instances, for example
	Village1, which can be later loaded from disk in subsequent sessions... and a name for the data point being 
	stored."""
	@classmethod
	def list(cls, inst, uid, name):
		shlv_ = cls.__get_shelf_(inst=inst, uid=uid)
		if name not in shlv_:
			shlv_[name] = list()
		return shlv_[name]

	@classmethod
	def dict(cls, inst, uid, name):
		shlv_ = cls.__get_shelf_(inst=inst, uid=uid)
		if name not in shlv_:
			shlv_[name] = dict()
		return shlv_[name]
