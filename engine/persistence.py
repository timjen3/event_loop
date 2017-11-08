import pickle
import gzip
import os


class IoStore:
	__LOADED_ = dict()

	@classmethod
	def __get_shelf_(cls, inst, uid):
		shelf_location_ = os.sep.join(["_bin", "{}".format(inst.__class__.__name__)])
		bin_name_ = "{}.bin".format(uid)
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

	@classmethod
	def get(cls, instance, method):
		shlv_ = cls.__get_shelf_(inst=instance, uid=instance.uid)
		if method.__name__ not in shlv_:
			target_obj = method(instance)
			shlv_[method.__name__] = target_obj
		target_obj = method(instance)
		from collections import defaultdict
		# if isinstance(target_obj, defaultdict):
		# 	print(shlv_[method.__name__])
		return shlv_[method.__name__]


def persisted(method):
	"""Add this decorator to a method to add persistence.
	The type returned by the method is what will be persisted."""
	def __target_store(s_, m_):
		return IoStore.get(instance=s_, method=m_)
	return lambda self, m=method: __target_store(self, m)
