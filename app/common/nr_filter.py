from typing import Optional, Dict
import ipaddress


# IP地址-筛选
def filter_by_ip(input_text):
    """
    根据输入的IP地址、IP地址范围或IP网络，返回一个包含有效IPv4地址的列表。
    Args:
        input_text: 一个字符串，包含一个或多个以逗号分隔的IP地址、IP地址范围或IP网络。
    Returns:
        一个包含有效IPv4地址的列表。即使输入单个IP地址或网络，也将返回一个单个元素的列表。
    """
    ip_list = []

    # 检查input_text是否为字符串，如果不是则直接返回False
    if not isinstance(input_text, str):
        return False

    # 对输入的内容以逗号分割进行for循环
    # 即使输入单个的IP地址，最后也会返回一个单个元素列表
    for i in input_text.split(','):
        i = i.strip()
        # print(i)
        try:
            # 尝试将输入解析为 IPv4Address ,单IP地址处理
            ip = str(ipaddress.IPv4Address(i))
            ip_list.append(ip)
        except ValueError:
            try:
                # 将输入拆分为两个 IP 地址
                start, end = i.split('-')
                # 尝试将输入解析为 IPv4Address
                ipaddress.IPv4Address(start.strip())
                ipaddress.IPv4Address(end.strip())
                start_ip = int(ipaddress.IPv4Address(start.strip()))
                end_ip = int(ipaddress.IPv4Address(end.strip()))
                for ip in range(start_ip, end_ip + 1):
                    ip = ipaddress.IPv4Address(ip)
                    ip_list.append(str(ip))
            except ValueError:
                try:
                    # 尝试将输入解析为 IPv4Network
                    net = ipaddress.IPv4Network(i)
                    # IP网段处理
                    if net.hostmask != '0.0.0.0':
                        for ip in net.hosts():
                            ip_list.append(str(ip))
                except ValueError as e:
                    # print(f'无法解析IP地址或IP地址范围或IP网络：{i}')
                    # 不能解析成单IP，IP范围，网段，直接返回False
                    return False

    return ip_list


def filter_nornir(nr: object, ip_value: Optional[str], platform_value: Optional[str],
                  model_value: Optional[str], area_value: Optional[str]) -> object:
    """
    根据提供的非None值过滤Nornir对象。
    Args:
        nr: 待过滤的Nornir对象。
        ip_value: 主机名（hostname）过滤值。
        platform_value: 平台（platform）过滤值。
        model_value: 模型（model）过滤值。
        area_value: 区域（area）过滤值。
    Returns:
        过滤后的Nornir对象或原始Nornir对象（如果没有提供有效的过滤条件）。
    """

    res = filter_by_ip(ip_value)
    if res:
        def ip_filter(host):
            """
            自定义过滤函数，检查主机名是否与给定IP地址列表中的任一IP地址相等。
            Args:
                host: Nornir Inventory中的主机对象。
            Returns:
                如果主机名与列表中的任一IP地址相等，返回True；否则返回False。
            """
            for ip in res:
                if ip == host.hostname:
                    # print(host)
                    return True

        nr = nr.filter(filter_func=ip_filter)
        # return nr


    else:
        # print('没有输入或输入的内容不能解析为IP地址>>>')
        # nr = nr.filter(hostname=ip_value)
        # return nr
        pass

    filter_dict: Dict[str, str] = {}

    for attr, value in zip(("platform", "model", "area"),
                           (platform_value, model_value, area_value)):
        if value is not None:
            filter_dict[attr] = value

    if filter_dict:
        # print('进行了platform_value, model_value, area_value 过滤')
        return nr.filter(**filter_dict)
    else:
        # print("没有进行了platform_value, model_value, area_value 过滤")
        # 返回未过滤的原始Nornir对象
        return nr