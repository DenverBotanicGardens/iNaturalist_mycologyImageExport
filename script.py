import requests

imageDirectory = "Q:/Research/Images(new)/ImagesInProcess/20240611_ILubow_iNatExport/"

def get_all_observation_photos(user_id, taxon_id):
    photos = []
    ids = []
    page = 1

    while True:
        url = f'https://api.inaturalist.org/v1/observations?user_id={user_id}&taxon_id={taxon_id}&has[]=photos&page={page}'
        response = requests.get(url)
        data = response.json()
        results = data['results']

        if not results:
            break

        for observation in results:
            observed_on_details_id = observation['id']
            for photo in observation['observation_photos']:
                photo_url = photo['photo']['url'].replace('square', 'original')
                photos.append(photo_url)
                ids.append(observed_on_details_id)
        
        page += 1

    return ids, photos

def save_to_batch(ids, photos, filename='download_images.bat'):
    with open(filename, 'w') as f:
        for i, (observed_on_details_id, photo_url) in enumerate(zip(ids, photos), start=1):
            filename = f'{imageDirectory}{observed_on_details_id}_{i}.jpg'
            f.write(f'curl {photo_url} -o {filename}\n')

    print(f"Batch file saved as {filename}")

def main():
    user_id = 'ilubow'
    taxon_id = 47170

    
    ids, photos = get_all_observation_photos(user_id, taxon_id)
    save_to_batch(ids, photos)

if __name__ == '__main__':
    main()
