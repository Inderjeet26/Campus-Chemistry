//
//  SearchViewController.m
//  Campus Chemistry
//
//  Created by Melissa Kendall on 12-03-18.
//  Copyright (c) 2012 University of Manitoba. All rights reserved.
//

#import "SearchViewController.h"
#import "SBJson.h"
#import "AppDelegate.h"

@interface SearchViewController ()

@end

@implementation SearchViewController

// CHANGED BY JMAN
@synthesize naviItem;
@synthesize navigationController;
@synthesize searchOptionViewController;

-(void)awakeFromNib {

}

// CHANGED BY JMAN

-(void)OptionButtonPressed
{
    [self.navigationController pushViewController:self.searchOptionViewController animated:YES];

}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) 
    {
        [self setTitle:@"Search"];
        
        // CHANGED BY JMAN
        if(searchOptionViewController == nil)
        {
            SearchOptionViewController *searchOptionView = [[SearchOptionViewController alloc] initWithNibName:@"SearchOptionViewController" bundle:nil];
            
            self.searchOptionViewController = searchOptionView;
        }
        
        //self.naviItem = [[UINavigationItem alloc] initWithTitle:@"Option"];
        
        UINavigationController *tempNavi = [[UINavigationController alloc] initWithRootViewController:self];
        [tempNavi setNavigationBarHidden:NO];
        navigationController = tempNavi;
        
       
    }
    return self;
}

- (NSInteger) tableView: (UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return [people count];
}

- (UITableViewCell *)tableView: (UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"Cell";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    if(cell == nil)
    {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier];
    } 
    
    if(indexPath.row < [people count])
    {
        cell.textLabel.text = [[people objectAtIndex:indexPath.row] firstName];
        cell.detailTextLabel.text = [[people objectAtIndex:indexPath.row] email];
    }
    
    return cell;
}

- (CGFloat) tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    return 50;
}

-(void) viewDidLoad
{
    appDelegate = [[UIApplication sharedApplication] delegate];

}

- (void) viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:YES];
    
    self.navigationItem.title = @"Search Results";
    NSString *ethnicity = @"Any";
    NSString *nationality = @"Any";
    NSString *city = @"Any";
    NSString *gender = @"Men/Women";
    NSString *orientation = @"Men/Women";
    NSString *minAge = @"18";
    NSString *maxAge = @"99";
    NSString *sort = @"Name";
    NSString *sortOrder = @"ASC";    
    NSString *userid = appDelegate.getUserEmail;
        
    if(![appDelegate.searchParams isEqualToString:@""])
    {
        NSString *paramString = appDelegate.searchParams;
        NSArray *arr = [paramString componentsSeparatedByString:@"&"];
        
        NSArray *temp = [[arr objectAtIndex:0] componentsSeparatedByString:@"="];
        minAge = [temp objectAtIndex:1];
        
        temp = [[arr objectAtIndex:1] componentsSeparatedByString:@"="];
        maxAge = [temp objectAtIndex:1];
        
        temp = [[arr objectAtIndex:2] componentsSeparatedByString:@"="];
        gender = [temp objectAtIndex:1];
        
        temp = [[arr objectAtIndex:3] componentsSeparatedByString:@"="];
        orientation = [temp objectAtIndex:1];
    }        

    //The below code should work for NSUrl
    responseData = [NSMutableData data];
    
    people = [[NSMutableArray alloc] init];
    
    NSString *args = [NSString stringWithFormat:@"ethnicity=%@&Birth_Country=%@&city=%@&gender=%@&orientation=%@&minAge=%@&maxAge=%@&sort=%@&sortOrder=%@&userid=%@", ethnicity,nationality,city,gender,orientation,minAge,maxAge,sort,sortOrder,userid];    
        
    NSString *msgLength = [NSString stringWithFormat:@"@d", [args length]];
    NSURL *url = [NSURL URLWithString:@"http://ec2-107-22-123-18.compute-1.amazonaws.com/python/search.wsgi"];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url cachePolicy:NSURLRequestReloadIgnoringCacheData timeoutInterval:60.0];
    [request addValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-type"];
    [request addValue:msgLength forHTTPHeaderField:@"Content-Length" ];
    [request setHTTPMethod:@"POST"];   
    [request setHTTPBody:[args dataUsingEncoding:NSUTF8StringEncoding]];
    
    NSURLResponse* response;
    NSError* error = nil;
    
    //Capturing server response
    NSData* result = [NSURLConnection sendSynchronousRequest:request  returningResponse:&response error:&error];   
    NSString *resultString = [[NSString alloc] initWithData:result encoding:NSUTF8StringEncoding];    
    
    //Parse json into dict
    SBJsonParser *jsonParser = [[SBJsonParser alloc] init];
    NSArray *jsonObjets = [jsonParser objectWithString:resultString error:&error];
    
    for (NSDictionary *dict in jsonObjets)
    {
        Person *person = [[Person alloc] init];
        
        [person setFirstName:[dict objectForKey:@"name"]];
        [person setAbout:[dict objectForKey:@"about"]];
        [person setDepartment:[dict objectForKey:@"department"]];
        [person setBodyType:[dict objectForKey:@"type"]];
        [person setPicture:[dict objectForKey:@"picture"]];
        [person setEmail:[dict objectForKey:@"email"]];
        
        [people addObject:person];
    }
    
    [self.tableView reloadData];
    
    // CHANGED BY JMAN

    //self.naviItem = [[UINavigationItem alloc] initWithTitle:@"Search Results"];
    
    UIBarButtonItem *optionButton = [[UIBarButtonItem alloc] initWithTitle:@"Option" style:UIBarButtonItemStylePlain target:self action:@selector(OptionButtonPressed)];          
    self.navigationItem.rightBarButtonItem = optionButton;    
    
    //self.navigationController.navigationItem = self.naviItem;
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
