from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime, timezone
from datetime import timedelta
from time import sleep
from urllib import parse as urlparse
import pytz
import asyncio
import aiohttp
import json
import re

domainName = "splus-wip3.pnistaging.com"
# domainName = "local-design.staples.com"
applicationPath = "/services/printing"
# productKey = "337c731e2cc14900"
# productKey = "880e9a0b0a627f97"
productKey = "550f7cadad98fe98"


async def loadCartPage(session, stress):
    async with session.get(f"https://{domainName}{applicationPath}/Cart", ssl=False, timeout=None) as response:
        data = await response.text()
        if stress is True:
            sleep(0.1)
            return None

        userIdPart = re.findall(
            "set_encUserID\('.*'\)", data)[0]
        encUserId = re.split("'", userIdPart)[1]
        sleep(0.1)
        async with session.get(f"https://{domainName}{applicationPath}/services/printing/Cart/Api/GetCartCount", ssl=False, timeout=None) as cartCount:
            await cartCount.text()
        async with session.post(f"https://{domainName}{applicationPath}/PC.WebServices/CartService.svc/GetCartItemCounts",
                                json={"encUserID": encUserId}, ssl=False, timeout=None) as apiResponse:
            data = await apiResponse.text()
        sleep(0.1)
    return None


async def stressCart(session):
    async with session.get(f"https://{domainName}{applicationPath}/Cart", ssl=False, timeout=None) as response:
        data = await response.text()
        userIdPart = re.findall(
            "set_encUserID\('.*'\)", data)[0]
        encUserId = re.split("'", userIdPart)[1]
        sleep(0.01)
        async with session.get(f"https://{domainName}{applicationPath}/services/printing/Cart/Api/GetCartCount", ssl=False, timeout=None) as cartCount:
            await cartCount.text()
        sleep(0.01)
        async with session.post(f"https://{domainName}{applicationPath}/PC.WebServices/CartService.svc/GetCartItemCounts",
                                json={"encUserID": encUserId}, ssl=False, timeout=None) as apiResponse:
            await apiResponse.text()
        sleep(0.01)

    async with session.get(f"https://{domainName}{applicationPath}/CartCheckout", ssl=False, timeout=None) as checkout:
        await checkout.text()
        sleep(0.01)
    return None


async def addToShoppingCart(session, groupKey, projectKey):
    data = {
        "GroupProjectKey": groupKey,
        "Projects": [
            {
                "ProjectKey": projectKey,
                "Quantity": 100
            }
        ]
    }
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/cart/AddGroupProjectToCart",
                            json=data, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def updateProject(session, projectKey):
    data = {
        "ProjectId": projectKey,
        "ProductKey": productKey,
        "SelectedOptions": {
            "Paper Type": "Gloss Stock",
            "SingleSided": "Disabled",
            "Color": "Full Color",
            "EditingFeatures": "Supports3DPreview",
            "IsExpress": "True"
        },
        "SelectedQuantity": 100
    }

    async with session.post(f"https://{domainName}{applicationPath}/api/v3/project/UpdateForReview/{projectKey}",
                            json=data, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def estimateShipMethods(session):
    tz = pytz.timezone("America/Los_Angeles")
    now = urlparse.quote(tz.localize(
        datetime.now()).isoformat(timespec="seconds"))
    url = f"https://{domainName}{applicationPath}/cart/api/ShippingMethods/Estimate?retailerProductSku=PNI_PostCards&quantity=100&price=45.99&orderDate={now}"
    async with session.get(url, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.05)
    return None


async def setShipMethod(session):
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/ShippingMethod",
                            json={"Id": "1tJHqTB,glCJdT3MYpet5WpqwOARm9GXE"}, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def setPickupLocation(session):
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/PickupLocation",
                            json={"RetailerStoreId": "0126"}, ssl=False, timeout=None) as response:
        await response.text()
        sleep(0.1)
        return None


async def getStorePromisedTime(session, isExress):
    body = {"Products": [{"ProductSku": "PNI_PostCards_SameDay", "Options": [
        {"Key": "IsExpress", "Value": f"{isExress}"}]}], "RetailerStoreId": "0126"}
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/StorePromiseTime", json=body, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.05)
    return None


async def loadUpsellPage(session, projectKey):
    async with session.get(f"https://{domainName}{applicationPath}/cart/api/Info", ssl=False, timeout=None) as cartInfo:
        await cartInfo.text()
    async with session.get(f"https://{domainName}{applicationPath}/legacy/StoreLocatorProxy/GetDefaultStore?latitude=47.65&longitude=-122.31&locale=en_US",
                           ssl=False, timeout=None) as defaultStore:
        await defaultStore.text()
    await estimateShipMethods(session)
    await getStorePromisedTime(session, True)
    await getStorePromisedTime(session, False)
    await getStorePromisedTime(session, True)
    await getStorePromisedTime(session, False)
    await getStorePromisedTime(session, True)
    await getStorePromisedTime(session, False)
    sleep(0.1)
    return None


async def navigateToCartPage(session, projectGroupKey, projectKey):
    await updateProject(session, projectKey)
    await addToShoppingCart(session, projectGroupKey, projectKey)
    return None


async def approveProject(session, projectKey):
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/project/Approve/{projectKey}",
                            json={}, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def getProjectInfo(session):
    async with session.get(f"https://{domainName}{applicationPath}/product/{productKey}/builder/", ssl=False, timeout=None) as response:
        data = await response.text()
        groupId = re.findall("[0-9]+", response.url.path)[0]
    sleep(0.1)
    summaryUrl = f"https://{domainName}{applicationPath}/api/builder/v3/project/group/summary/{groupId}"
    async with session.get(summaryUrl, ssl=False, timeout=None) as jsonResponse:
        data = json.loads(await jsonResponse.text())

    return (groupId, data["SubProjects"][0]["ProjectKey"])


async def setupAsRik(session):
    async with session.get(f"https://{domainName}{applicationPath}/legacy/station/6B696F736b5F72696B/126/redirect/",
                           ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def visitSite(id):
    async with aiohttp.ClientSession() as session:
        await setupAsRik(session)
        projectInfo = await getProjectInfo(session)
        await approveProject(session, projectInfo[1])
        await setPickupLocation(session)
        print(f"Job {id} will go to shopping cart")
        for _ in range(10):
            await navigateToCartPage(session, projectInfo[0], projectInfo[1])
            await loadCartPage(session, False)

        print(
            f"Beging stress at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ...")
        # end = datetime.now() + timedelta(minutes=10)
        end = datetime.now() + timedelta(hours=12)
        try:
            while datetime.now() < end:
                await stressCart(session)
        except:
            print(f"Job {id} run into issue")
        finally:
            print(
                f"End stress at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ...")
    return id


async def createConnections():
    print(
        f"Start at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tasks = []
    for jobId in range(25):
        task = asyncio.ensure_future(visitSite(jobId))
        tasks.append(task)

    await asyncio.gather(*tasks, return_exceptions=True)
    for t in tasks:
        try:
            id = t.result()
            print(
                f"Finished {id} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            print(f"Job {id} run into issue")
            continue


def launch(p):
    if p > 0:
        sleep(p*300)
    asyncio.run(createConnections())
    return p


def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        _ = executor.map(launch, range(1000))


if __name__ == "__main__":
    main()
