#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/string.h>

#define DEVICE_NAME "kvault"

MODULE_LICENSE("UNLICENSED");
MODULE_AUTHOR("OddNorseman & Zopazz");
MODULE_DESCRIPTION("Kernel Vault");
MODULE_VERSION("0.1");

typedef struct {
    char *key;
    int key_len;
    char *value;
    int value_len;
} vault_entry;

#define VAULT_SIZE 10
#define MAX_STRING_SIZE 255
vault_entry vault[VAULT_SIZE];

static int find_entry(char *key) {
    int i;
    for (i = 0; i < VAULT_SIZE; i++) {
        if (vault[i].key && strncmp(vault[i].key, key, strlen(key)) == 0) {
            return i;
        }
    }
    return -1;
}

static int find_empty_entry(void) {
    int i;
    for (i = 0; i < VAULT_SIZE; i++) {
        if (vault[i].key == NULL) {
            return i;
        }
    }
    return -1;
}

static long add_entry(vault_entry data) {
    //Copying the user space pointers in the vault_entry struct to kernel space
    char *key = kmalloc(data.key_len, GFP_KERNEL);
    char *value = kmalloc(data.value_len, GFP_KERNEL);
    copy_from_user(key, data.key, data.key_len);
    copy_from_user(value, data.value, data.value_len);
    data.key = key;
    data.value = value;

    int index = find_empty_entry();
    if (index == -1) {
        printk(KERN_ERR "No space in vault\n");
        return -ENOSPC;
    }
    if (find_entry(data.key) != -1) {
        printk(KERN_ERR "Key already exists\n");
        return -EEXIST;
    }
    printk(KERN_DEBUG "Adding entry with key: %s and value: %s\n", data.key, data.value);
    vault[index].key = data.key;
    vault[index].value = data.value;
    vault[index].key_len = data.key_len;
    vault[index].value_len = data.value_len;
    return 0;
}

static long get_entry(vault_entry data, unsigned long arg) {
    //Copying the user space pointers in the vault_entry struct to kernel space
    char *key = kmalloc(data.key_len, GFP_KERNEL);
    strncpy_from_user(key, data.key, data.key_len);
    
    int index = find_entry(key);
    if (index == -1) {
        printk(KERN_ERR "Entry not found\n");
        return -ENOENT;
    }
    data.value_len = vault[index].value_len;
    printk(KERN_DEBUG "Getting entry with key: %s, value: %s, len: %i", key, vault[index].value, data.value_len);
    int res = copy_to_user((void *) data.value, vault[index].value, data.value_len);
    data.value_len = data.value_len;
    return res+copy_to_user((void *)arg, (void *)&data, sizeof(data));
}

static long delete_entry(vault_entry data) {
    //Copying the user space pointers in the vault_entry struct to kernel space
    char *key = kmalloc(data.key_len, GFP_KERNEL);
    copy_from_user(key, data.key, data.key_len);

    int index = find_entry(key);
    if (index == -1) {
        printk(KERN_ERR "Entry not found\n");
        return -ENOENT;
    }
    kfree(vault[index].key);
    kfree(vault[index].value);

    printk(KERN_DEBUG "Deleted entry with key: %s", key);
    return 0;
}

static long update_entry(vault_entry data) {
    //Copying the user space pointers in the vault_entry struct to kernel space
    char *key = kmalloc(data.key_len, GFP_KERNEL);
    char *value = kmalloc(data.value_len, GFP_KERNEL);
    copy_from_user(key, data.key, data.key_len);
    copy_from_user(value, data.value, data.value_len);
    data.key = key;
    data.value = value;

    int index = find_entry(data.key);
    if (index == -1) {
        printk(KERN_ERR "Entry not found\n");
        return -ENOENT;
    }
    printk(KERN_INFO "Updating entry with key '%s'\n", data.key);
    if (data.value_len != vault[index].value_len) {
        printk(KERN_INFO "Unequal size! Freeing and allocating. %d != %d\n", data.value_len, vault[index].value_len);
        kfree(vault[index].value);
        vault[index].value = kmalloc(data.value_len, GFP_KERNEL);
        vault[index].value_len = data.value_len;
    }
    printk(KERN_INFO "Copying from %lx to %lx\n", data.value, vault[index].value);
    memcpy(vault[index].value, data.value, data.value_len);
    return 0;
}

static long device_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    uint64_t res = -EINVAL;
    vault_entry data;
    if(copy_from_user((void *)&data, (void *) arg, sizeof(data))){
        printk(KERN_ERR "copy_from_user failed\n");
        goto exit;
    }

    if (data.key_len > MAX_STRING_SIZE || data.key_len < 1 || data.value_len > MAX_STRING_SIZE || data.value_len < 0) {
        res = -EINVAL;
        printk(KERN_ERR "String invalid size\n");
        goto exit;
    }

    if (cmd == 0x13371) res = add_entry(data);
    else if (cmd == 0x13372) res = get_entry(data, arg);
    else if (cmd == 0x13373) res = delete_entry(data);
    else if (cmd == 0x13374) res = update_entry(data);
exit:
    return res;
}


static struct file_operations fips = {
  .owner = THIS_MODULE,
  .unlocked_ioctl = device_ioctl,
};

static int __init module_initialize(void)
{
    int register_error;
    printk(KERN_INFO "Initializing KVault.\n");
    register_error = register_chrdev('k', DEVICE_NAME, &fips);
    if (register_error) {
      printk(KERN_ERR "Initialization failed!\n");
      return register_error;
    }
    printk(KERN_INFO "KVault Loaded\n");
    return 0;
}

static void __exit module_cleanup(void)
{
    unregister_chrdev('k', DEVICE_NAME);
    printk(KERN_INFO "KVault Unloaded\n");
}

module_init(module_initialize);
module_exit(module_cleanup);